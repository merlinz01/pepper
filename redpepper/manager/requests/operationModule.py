import base64
import os
from typing import BinaryIO

from redpepper.manager.manager import AgentConnection
from redpepper.manager.requests import RequestError


def call(conn: AgentConnection, name: str, existing_mtime: float, existing_size: int):
    try:
        path = conn.manager.data_manager.get_operation_module_path(conn.agent_id, name)
    except ValueError as e:
        raise RequestError(str(e)) from e
    try:
        stat = os.stat(path)
        mtime = stat.st_mtime
        size = stat.st_size
        if mtime == existing_mtime and size == existing_size:
            return {"changed": False}
    except FileNotFoundError:
        raise RequestError(f"Operation module not found: {name}") from e
    with open(path, "rb") as f:
        f: BinaryIO
        mtime = os.fstat(f.fileno()).st_mtime
        data = f.read()
    if len(data) > 32 * 1024:
        raise RequestError(f"Operation module too large: {name}") from e
    return {
        "changed": True,
        "data": base64.b64encode(data).decode("utf-8"),
        "mtime": mtime,
        "size": len(data),
    }
