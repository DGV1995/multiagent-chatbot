from langgraph_supervisor import create_supervisor

from backend.agents.booking import flight_agent, hotel_agent
from backend.agents.maths import maths_agent
from backend.agents.openai_client import get_openai_client

_supervisor = None


def get_supervisor():
    """
    Lazily initializes and returns a singleton swarm supervisor instance with the needed agents.
    """
    global _supervisor

    if not _supervisor:
        _supervisor = create_supervisor(
            model=get_openai_client(),
            agents=[maths_agent, flight_agent, hotel_agent],
            prompt="You are a supervisor that coordinates multiple agents to solve complex problems. When users ask for cheapest travel combinations: 1) Use flight_agent to get all flight options, 2) Use hotel_agent to get all hotel options, 3) Use maths_agent to calculate and compare total prices for matching destinations, 4) Present the cheapest combination to the user, 5) If user confirms booking, use flight_agent and hotel_agent to book the specific options. You can remember information between steps and coordinate the agents to work together.",
            name="supervisor",
        ).compile()

    return _supervisor
