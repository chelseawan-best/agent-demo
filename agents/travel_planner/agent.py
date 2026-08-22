"""Minimal single-agent travel planner.

The project keeps the model/tool loop visible on purpose. The travel tools are
deterministic placeholders; each can later be replaced by a real API adapter.
"""

from typing import Any

from langchain.agents import create_agent
from langchain_core.tools import tool

from utils.models import model


@tool
def search_flights(origin: str, destination: str, date: str) -> list[dict[str, Any]]:
    """Return candidate flights for a route and departure date."""
    return [
        {"id": "FL-001", "airline": "Demo Air", "origin": origin,
         "destination": destination, "date": date, "price": 420,
         "stops": 0, "departure": "08:20", "arrival": "12:30"},
        {"id": "FL-002", "airline": "Budget Air", "origin": origin,
         "destination": destination, "date": date, "price": 310,
         "stops": 1, "departure": "14:10", "arrival": "19:30"},
    ]


@tool
def search_hotels(city: str, checkin: str, checkout: str) -> list[dict[str, Any]]:
    """Return candidate hotels for a city and date range."""
    return [
        {"id": "HT-001", "name": f"Central Hotel {city}",
         "city": city, "checkin": checkin, "checkout": checkout,
         "price_per_night": 120, "rating": 4.5, "area": "City center"},
        {"id": "HT-002", "name": f"Budget Inn {city}",
         "city": city, "checkin": checkin, "checkout": checkout,
         "price_per_night": 80, "rating": 4.1, "area": "Near metro"},
    ]


@tool
def search_activities(city: str, interest: str) -> list[dict[str, Any]]:
    """Return candidate activities matching an interest in a city."""
    return [
        {"id": "AC-001", "name": f"{interest.title()} walk in {city}",
         "city": city, "duration_hours": 3, "price": 25},
        {"id": "AC-002", "name": f"{city} cultural museum",
         "city": city, "duration_hours": 2, "price": 18},
    ]


SYSTEM_PROMPT = """You are a travel planning assistant.
Use the available tools to research flights, hotels, and activities before
making claims. Never invent prices or availability. Return a concise plan with
the selected options, a simple budget, and a day-by-day outline. This first
version is research-only: never book anything.
"""


agent = create_agent(
    model=model,
    tools=[search_flights, search_hotels, search_activities],
    system_prompt=SYSTEM_PROMPT,
)

