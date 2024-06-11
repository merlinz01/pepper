from redpepper.manager.manager import AgentConnection
from redpepper.manager.requests import RequestError


def call(conn: AgentConnection, name: str):
    try:
        return conn.manager.data_manager.get_data_for_agent(conn.agent_id, name)
    except KeyError:
        raise RequestError(f"Data not found: {name}")
