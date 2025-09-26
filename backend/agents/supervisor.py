from langgraph_supervisor import create_supervisor

from backend.agents.maths import maths_agent
from backend.agents.openai_client import get_openai_client

_supervisor = None


def get_supervisor():
    """
    Lazily initializes and returns a singleton supervisor instance with the needed agents.
    """
    global _supervisor

    if not _supervisor:
        _supervisor = create_supervisor(
            agents=[maths_agent],
            model=get_openai_client(),
            prompt="You have to help the user with their query by deciding which agent to use.",
        )

    return _supervisor.compile()
