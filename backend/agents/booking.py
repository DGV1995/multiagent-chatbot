from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

from backend.agents.openai_client import get_openai_client


# Flight tools
@tool
def book_flight(destination: str, date: str, details: dict) -> str:
    """
    Books a flight to the destination on the specified date.
    It gets the booking details as a dict from the search_bookings_options tool.
    """
    print("[TOOL] book_flight executed")
    return f"Flight booked to {destination} on {date}. Details: {str(details)}"


@tool
def search_flights_options(date: str) -> dict:
    """
    Searches for available flight options on the specified date.
    Returns a hardcoded dict with several booking options for matching cities.
    """
    print("[TOOL] search_flights_options executed")
    cities = ["New York", "London", "Paris"]
    options = [
        {
            "flight": "Flight A",
            "destination": cities[0],
            "date": date,
            "price": 120.0,
            "departure_time": "08:00",
            "arrival_time": "10:00",
        },
        {
            "flight": "Flight B",
            "destination": cities[1],
            "date": date,
            "price": 150.0,
            "departure_time": "12:00",
            "arrival_time": "14:00",
        },
        {
            "flight": "Flight C",
            "destination": cities[2],
            "date": date,
            "price": 180.0,
            "departure_time": "18:00",
            "arrival_time": "20:00",
        },
    ]
    return {"options": options}


# Hotel tools
@tool
def book_hotel(destination: str, date: str, details: dict) -> str:
    """
    Books a hotel in the destination on the specified date.
    It gets the booking details as a dict from the search_hotels_options tool.
    """
    print("[TOOL] book_hotel executed")
    return f"Hotel booked in {destination} on {date}. Details: {str(details)}"


@tool
def search_hotels_options(date: str) -> dict:
    """
    Searches for available hotel options on the specified date.
    Returns a hardcoded dict with several hotel options for matching cities.
    """
    print("[TOOL] search_hotels_options executed")
    cities = ["New York", "London", "Paris"]
    options = [
        {
            "hotel": "Hotel Alpha",
            "destination": cities[0],
            "date": date,
            "price": 80.0,
            "check_in": "15:00",
            "check_out": "11:00",
        },
        {
            "hotel": "Hotel Beta",
            "destination": cities[1],
            "date": date,
            "price": 100.0,
            "check_in": "16:00",
            "check_out": "12:00",
        },
        {
            "hotel": "Hotel Gamma",
            "destination": cities[2],
            "date": date,
            "price": 120.0,
            "check_in": "14:00",
            "check_out": "10:00",
        },
    ]
    return {"options": options}


# LLM initialization
llm = get_openai_client()


# Create specialized agents
flight_tools = [book_flight, search_flights_options]
hotel_tools = [book_hotel, search_hotels_options]

flight_agent = create_react_agent(
    llm,
    flight_tools,
    prompt="You are a helpful flight assistant specialized in flight bookings and flight searches. You can search for available flights and book them.",
    name="flight_assistant",
)

hotel_agent = create_react_agent(
    llm,
    hotel_tools,
    prompt="You are a helpful hotel assistant specialized in hotel bookings and hotel searches. You can search for available hotels and book them.",
    name="hotel_assistant",
)
