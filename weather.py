import requests
from config import CITY, STATE, COUNTRY

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Light Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Light Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Heavy Rain Showers",
    95: "Thunderstorm",
}

def get_forecast():
    latitude, longitude = get_coordinates()

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&hourly=temperature_2m,precipitation_probability,weather_code"
        "&temperature_unit=fahrenheit"
        "&forecast_days=1"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()["hourly"]

    forecast = []

    for i in range(min(24, len(data["time"]))):
        code = data["weather_code"][i]

        forecast.append({
            "time": data["time"][i],
            "temperature": data["temperature_2m"][i],
            "precipitation_probability": data["precipitation_probability"][i],
            "condition": WEATHER_CODES.get(code, f"Unknown ({code})")
        })

    return forecast


def get_coordinates():
    url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={CITY}"
        "&count=10"
        "&language=en"
        "&format=json"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    if "results" not in data:
        raise ValueError(f"Could not find city: {CITY}")

    for result in data["results"]:
        state_match = result.get("admin1", "").lower() == STATE.lower()
        country_match = result.get("country", "").lower() == COUNTRY.lower()

        if state_match and country_match:
            return result["latitude"], result["longitude"]

    raise ValueError(f"Could not find location: {CITY}, {STATE}, {COUNTRY}")


def get_weather():
    latitude, longitude = get_coordinates()

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,precipitation,rain,weather_code,wind_speed_10m"
        "&hourly=temperature_2m,precipitation_probability,weather_code"
        "&temperature_unit=fahrenheit"
        "&wind_speed_unit=mph"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()["current"]

    return {
        "temperature": data["temperature_2m"],
        "condition": WEATHER_CODES.get(
            data["weather_code"],
            f"Unknown ({data['weather_code']})"
        ),
        "rain": data["rain"],
        "precipitation": data["precipitation"],
        "wind_speed": data["wind_speed_10m"],
    }