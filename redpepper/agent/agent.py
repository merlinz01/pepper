"""RedPepper Agent"""

import importlib.util
import json
import logging
import os
import ssl
import subprocess
import sys
import traceback

import trio

from redpepper.agent.config import load_agent_config
from redpepper.agent.tasks import Task, topological_sort
from redpepper.common.connection import Connection
from redpepper.common.messages_pb2 import CommandResult, Message, MessageType
from redpepper.common.slot import Slot
from redpepper.common.tls import load_tls_context
from redpepper.operations import Result

logger = logging.getLogger(__name__)


class Agent:
    """RedPepper Agent"""

    def __init__(self, config=None, config_file=None):
        self.config = config or load_agent_config(config_file)
        self.conn = None
        self.data_slots: dict[int, Slot] = {}
        self.last_message_id = 100
        self.tls_context: ssl.SSLContext = load_tls_context(
            ssl.Purpose.SERVER_AUTH,
            self.config["tls_cert_file"],
            self.config["tls_key_file"],
            self.config["tls_key_password"],
            verify_mode=self.config["tls_verify_mode"],
            check_hostname=self.config["tls_check_hostname"],
            cafile=self.config["tls_ca_file"],
            capath=self.config["tls_ca_path"],
            cadata=self.config["tls_ca_data"],
        )

    async def connect(self):
        host = self.config["manager_host"]
        port = self.config["manager_port"]
        self.remote_address = (host, port)
        logger.info("Connecting to manager at %s:%s", host, port)
        try:
            stream = await trio.open_ssl_over_tcp_stream(
                host, port, ssl_context=self.tls_context
            )
        except ConnectionError:
            logger.error("Failed to connect to server", exc_info=1)
            raise
        self.conn = Connection(
            stream, self.config["ping_timeout"], self.config["ping_interval"]
        )

    async def handshake(self):
        hello_slot = Slot()
        self.conn.message_handlers[MessageType.SERVERHELLO] = hello_slot.set
        hello = Message()
        hello.type = MessageType.CLIENTHELLO
        hello.client_hello.clientID = self.config["agent_id"]
        hello.client_hello.auth = self.config["agent_secret"]
        logger.debug("Sending client hello message to manager")
        await self.conn.send_message(hello)
        try:
            server_hello = await hello_slot.get(self.config["hello_timeout"])
        except trio.TooSlowError:
            logger.error("Handshake timed out")
            await self.conn.close()
            return
        del self.conn.message_handlers[MessageType.SERVERHELLO]
        if server_hello.server_hello.version != 1:
            logger.error(
                "Unsupported server version %s", server_hello.server_hello.version
            )
            await self.conn.close()
            return
        self.conn.message_handlers[MessageType.COMMAND] = self.handle_command
        self.conn.message_handlers[MessageType.DATARESPONSE] = self.handle_data_response

    async def handle_command(self, message):
        cmdtype = message.command.type
        try:
            kw = json.loads(message.command.data)
        except json.JSONDecodeError:
            logger.error("Failed to decode command data")
            self.send_command_progress(
                message.command.commandID,
                CommandResult.Status.FAILURE,
                False,
                "Failed to decode command data",
            )
            return
        args = kw.pop("[args]", [])
        await trio.to_thread.run_sync(
            self._run_command,
            message.command.commandID,
            cmdtype,
            args,
            kw,
        )

    def _run_command(self, commandID, cmdtype, args, kw):
        if cmdtype == "state":
            self.run_state(commandID, *args, _send_status=True, **kw)
            return
        try:
            self.send_command_progress(commandID, current=0, total=1)
            result = self.run_command(cmdtype, args, kw)
            status = (
                CommandResult.Status.SUCCESS
                if result.succeeded
                else CommandResult.Status.FAILED
            )
            self.send_command_progress(commandID, current=1, total=1)
            self.send_command_result(commandID, status, result.changed, str(result))
        except Exception:
            output = f"Failed to execute command {cmdtype!r}:\n{traceback.format_exc()}"
            self.send_command_result(
                commandID, CommandResult.Status.FAILED, False, output
            )

    def run_command(self, cmdtype, args, kw):
        logger.debug("Preparing to run operation %s", cmdtype)
        parts = cmdtype.split(".", 1)
        if (
            len(parts) != 2
            or not parts[0].isidentifier()
            or not parts[1].isidentifier()
        ):
            raise ValueError("Invalid operation type")
        module_name, class_name = parts
        logger.debug("Looking for operation module %s", module_name)
        try:
            module = importlib.import_module("redpepper.operations." + module_name)
        except ImportError as e:
            cached_path = os.path.join(
                self.config["operation_modules_cache_dir"], module_name + ".py"
            )
            if not os.path.isfile(cached_path):
                ok, data = self.request_data("operation_module", module_name)
                if not ok:
                    logger.error(
                        "Failed to request operation module %s: %s", module_name, data
                    )
                    raise ValueError(
                        f"Failed to request operation module {module_name}: {data}"
                    )
                with open(cached_path, "w") as f:
                    f.write(data)
            try:
                spec = importlib.util.spec_from_file_location(module_name, cached_path)
                module = importlib.util.module_from_spec(spec)
                sys.modules["redpepper.operations." + module_name] = module
                spec.loader.exec_module(module)
            except Exception as e:
                logger.error("Failed to load operation module %s: %s", module_name, e)
                raise
        logger.debug("Looking for operation class %s", class_name)
        try:
            command_class = getattr(module, class_name)
        except AttributeError:
            logger.error("Operation class not found %s", class_name)
            raise ValueError(
                f"Operation class {class_name} not found in module {module_name}"
            )
        cond = kw.pop("if", None)
        logger.debug("Checking operation condition %r", cond)
        try:
            if not self.evaluate_condition(cond):
                logger.debug("Operation condition not met for %s", cmdtype)
                result = Result(cmdtype)
                result.succeeded = True
                result += "Condition not met"
                return result
        except Exception as e:
            logger.error("Failed to evaluate condition %s", e, exc_info=1)
            raise
        logger.debug("Instantiating operation class %s", cmdtype)
        try:
            command = command_class(*args, **kw)
        except Exception as e:
            logger.error("Failed to instantiate operation class %s", e, exc_info=1)
            raise
        logger.debug("Running operation %s", cmdtype)
        try:
            result = command.ensure(self)
        except Exception as e:
            logger.error("Operation failed %s", e, exc_info=1)
            raise
        if not isinstance(result, Result):
            logger.warn("Operation returned a non-Result object: %r", result)
            result = Result(cmdtype)
            result.succeeded = False
            result += "Operation returned a non-Result object: %r" % result
        logger.debug("Operation result: %s", result)
        return result

    def run_state(self, commandID, state="", _send_status=False):
        # TODO: This could be made a bit less hacky by putting
        # the state data retrieval and result (progress too?) reporting in _run_command
        def error(msg):
            logger.error(msg, exc_info=1)
            if _send_status:
                self.send_command_result(
                    commandID, CommandResult.Status.FAILED, False, msg
                )
            else:
                raise ValueError(msg)

        if isinstance(state, str):
            state_name = "State" + (" " + state if state else "")
            ok, data = self.request_data("state", state)
            if not ok:
                return error(f"Failed to retrieve state {state}: {data}")
            state = json.loads(data)
            if not isinstance(state, dict):
                return error(f"State {state} is not a dictionary")
        else:
            state_name = None  # not used or displayed
            state = {state_name: state}
        tasks = {}
        for key, st in state.items():
            if not isinstance(st, (dict, list)):
                return error(f"State {state} task {key} is not a dictionary")
            if isinstance(st, list):
                requirements = set()
                for i, item in enumerate(st, 1):
                    if not isinstance(item, dict):
                        return error(
                            f"State {state} task {key} item {i} is not a dictionary"
                        )
                    req = item.pop("require", ())
                    if isinstance(req, str):
                        requirements.add(req)
                    else:
                        requirements.update(req)
                tasks[key] = Task(key, st, requirements)
            else:
                requirements = st.pop("require", ())
                if isinstance(requirements, str):
                    requirements = {requirements}
                tasks[key] = Task(key, st, set(requirements))
        try:
            sorted_tasks = topological_sort(tasks)
        except ValueError as e:
            return error(f"Failed to sort states by dependencies: {e}")
        i = 0

        def flatten(tasks):
            # Yield single tasks from a list of tasks that may contain task groups
            for task in tasks:
                if isinstance(task.data, list):
                    for i, subtaskdata in enumerate(task.data, 1):
                        subtask = Task(f"{task.name} #{i}", subtaskdata, None)
                        # Allow more than one level of grouping
                        yield from flatten([subtask])
                else:
                    yield task

        sorted_tasks = list(flatten(sorted_tasks))

        result = Result(state_name)
        if _send_status:
            self.send_command_progress(
                commandID,
                current=0,
                total=len(sorted_tasks),
            )
        for task in sorted_tasks:
            result += f"\nRunning state {task.name}:"
            data = task.data
            onchange = data.pop("onchange", None)
            try:
                cmd_result = self.run_command(data.pop("type"), [], data)
            except Exception:
                if not _send_status:
                    raise
                else:
                    cmd_result = Result(task.name)
                    cmd_result.fail(
                        f"Failed to execute state {task.name}:\n{traceback.format_exc()}"
                    )
            result.update(cmd_result)
            i += 1
            if not result.succeeded:
                break
            if onchange and cmd_result.changed:
                onchange_result = self.run_state(
                    commandID, onchange, _send_status=False
                )
                result.update(onchange_result)
                if not result.succeeded:
                    break
            if _send_status:
                self.send_command_progress(
                    commandID,
                    current=i,
                    total=len(sorted_tasks),
                )
        if _send_status:
            self.send_command_result(
                commandID,
                (
                    CommandResult.Status.SUCCESS
                    if result.succeeded
                    else CommandResult.Status.FAILED
                ),
                result.changed,
                str(result),
            )
        return result

    def send_command_progress(self, command_id, current=1, total=1):
        message = Message()
        message.type = MessageType.COMMANDPROGRESS
        message.progress.commandID = command_id
        message.progress.current = current
        message.progress.total = total
        self.conn.send_message_threadsafe(message)

    def send_command_result(self, command_id, status, changed, output):
        message = Message()
        message.type = MessageType.COMMANDRESULT
        message.result.commandID = command_id
        message.result.status = status
        message.result.changed = changed
        message.result.output = output
        self.conn.send_message_threadsafe(message)

    def request_data(self, dtype, data):
        message = Message()
        message.type = MessageType.DATAREQUEST
        self.last_message_id += 1
        message.data_request.requestID = self.last_message_id
        message.data_request.type = dtype
        message.data_request.data = data
        self.data_slots[message.data_request.requestID] = slot = Slot(type="thread")
        self.conn.send_message_threadsafe(message)
        try:
            response = slot.get_threadsafe(self.config["data_request_timeout"])
        except trio.TooSlowError:
            return False, "Data request timed out"
        if response.data_response.WhichOneof("data") == "string":
            return response.data_response.ok, response.data_response.string
        elif response.data_response.WhichOneof("data") == "bytes":
            return response.data_response.ok, response.data_response.bytes
        else:
            return False, "Invalid data response"

    async def handle_data_response(self, message):
        logger.debug("Received data response: %r", message.data_response)
        slot = self.data_slots.get(message.data_response.requestID, None)
        if not slot:
            logger.error(
                "Data response for unknown request ID %s",
                message.data_response.requestID,
            )
            return
        await slot.set(message)
        del self.data_slots[message.data_response.requestID]

    def evaluate_condition(self, condition):
        if not condition:
            return True
        if isinstance(condition, dict) and len(condition) > 1:
            raise ValueError("Use a list for multiple conditions")
        if isinstance(condition, list):
            logger.debug("Evaluating all conditions in list: %r", condition)
            return all(self.evaluate_condition(c) for c in condition)
        if not isinstance(condition, dict):
            raise ValueError("Condition must be a single key-value pair")
        k = next(iter(condition))
        v = condition[k]
        logger.debug("Evaluating condition %r: %r", k, v)
        if k == "not":
            return not self.evaluate_condition(v)
        negate = False
        words = k.split()
        if words[0] == "not":
            negate = True
            words.pop(0)
        ctype = words.pop(0)
        logger.debug("Condition type: %s", ctype)
        if ctype == "true":
            if words:
                raise ValueError("Invalid condition name: {k!r}")
            if v is not None:
                raise ValueError("Condition true does not take a value")
            return not negate
        if ctype == "false":
            if words:
                raise ValueError("Invalid condition name: {k!r}")
            if v is not None:
                raise ValueError("Condition false does not take a value")
            return negate
        if ctype == "all":
            if words:
                raise ValueError("Invalid condition name: {k!r}")
            if not isinstance(v, list):
                raise ValueError("Value for all condition must be a list")
            return not negate if all(self.evaluate_condition(c) for c in v) else negate
        if ctype == "any":
            if words:
                raise ValueError("Invalid condition name: {k!r}")
            if not isinstance(v, list):
                raise ValueError("Value for any condition must be a list")
            return not negate if any(self.evaluate_condition(c) for c in v) else negate
        if ctype == "py":
            if words:
                raise ValueError("Invalid condition name: {k!r}")
            return not negate if eval(v) else negate
        if ctype == "cmd":
            retcodes = [0]
            if words:
                retcodes = [int(w) for w in words.pop(0).split(",")]
            if words:
                raise ValueError(f"Invalid condition name: {k!r}")
            if not isinstance(v, str):
                raise ValueError(
                    f"Invalid command condition value type: {type(v).__name__}"
                )
            success = False
            logger.debug("Running condition command: %s", v)
            try:
                rc = subprocess.call(v, shell=True)
                success = rc in retcodes
            except Exception as e:
                success = False
            return not negate if success else negate
        if ctype == "file":
            verb = "exists"
            if words:
                verb = words.pop(0)
            if words:
                raise ValueError(f"Invalid condition name: {k!r}")
            if verb == "exists":
                logger.debug("Checking if file exists: %s", v)
                return not negate if os.path.exists(v) else negate
            else:
                raise ValueError(f"Invalid file condition verb {verb}")
        logger.error("Invalid condition name: %s", k)
        raise ValueError(f"Invalid condition name: {k!r}")

    async def run(self):
        """Run the agent"""
        await self.connect()
        async with trio.open_nursery() as nursery:
            nursery.start_soon(self.conn.run)
            nursery.start_soon(self.handshake)
