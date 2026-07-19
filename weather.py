"""
weather.py
Core logic for looking up weather by city name.
Uses the free Open-Meteo API (no API key required):
  - Geocoding: turn a city name into latitude/longitude
  - Forecast:  turn latitude/longitude into current weather
"""

import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo returns a numeric weather code; this maps it to something readable.
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Rain showers", 95: "Thunderstorm",
}


def get_coordinates(city_name: str) -> dict:
    """
    Look up a city name and return its coordinates.
    Returns: {"name": str, "latitude": float, "longitude": float}
    Raises: ValueError if the city can't be found.
    """
    response = requests.get(GEOCODE_URL, params={"name": city_name, "count": 1})
    response.raise_for_status()
    data = response.json()

    results = data.get("results")
    if not results:
        raise ValueError(f"Could not find a city named '{city_name}'")

    top = results[0]
    return {
        "name": f"{top['name']}, {top.get('country', '')}".strip(", "),
        "latitude": top["latitude"],
        "longitude": top["longitude"],
    }


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather for a coordinate.
    Returns: {"temperature_c": float, "windspeed_kmh": float, "condition": str}
    """
    response = requests.get(FORECAST_URL, params={
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
    })
    response.raise_for_status()
    current = response.json()["current_weather"]

    return {
        "temperature_c": current["temperature"],
        "windspeed_kmh": current["windspeed"],
        "condition": WEATHER_CODES.get(current["weathercode"], "Unknown"),
    }


def lookup(city_name: str) -> dict:
    """Convenience function: city name in, full weather report out."""
    place = get_coordinates(city_name)
    weather = get_weather(place["latitude"], place["longitude"])
    return {**place, **weather}