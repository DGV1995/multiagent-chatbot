from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

from backend.agents.openai_client import get_openai_client


@tool
def book_flight(destination: str, date: str, details: dict) -> str:
    """
    Books a flight to the destination on the specified date.
    It gets the booking details as a dict from the search_bookings_options tool.
    """
    # Implementation goes here
    return f"Flight booked to {destination} on {date}. Details: {str(details)}"


@tool
def search_bookings_options(date: str, destination: str) -> dict:
    """
    Searches for available flight options to the destination on the specified date.
    Returns a hardcoded dict with several booking options.
    """
    options = [
        {
            "flight": "Flight A",
            "destination": destination,
            "date": date,
            "price": 120.0,
            "departure_time": "08:00",
            "arrival_time": "10:00",
        },
        {
            "flight": "Flight B",
            "destination": destination,
            "date": date,
            "price": 150.0,
            "departure_time": "12:00",
            "arrival_time": "14:00",
        },
        {
            "flight": "Flight C",
            "destination": destination,
            "date": date,
            "price": 180.0,
            "departure_time": "18:00",
            "arrival_time": "20:00",
        },
    ]

    return {"options": options}


# List of tools for bookings
bookings_tools = [book_flight, search_bookings_options]

# LLM initialization (you can change the model to the one you have configured)
llm = get_openai_client()

# ReAct agent initialization using create_react_agent
bookings_agent = create_react_agent(
    llm,
    bookings_tools,
    prompt="You are a helpful bookings assistant.",
    name="bookings_agent",
)
