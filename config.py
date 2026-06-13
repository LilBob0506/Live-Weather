from dotenv import load_dotenv
import os

load_dotenv()

CITY = os.getenv("CITY")
STATE = os.getenv("STATE")
COUNTRY = os.getenv("COUNTRY")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", 10))
TEMP_CHANGE_THRESHOLD = int(os.getenv("TEMP_CHANGE_THRESHOLD", 5))
WIND_CHANGE_THRESHOLD = int(os.getenv("WIND_CHANGE_THRESHOLD", 10))

SEVERE_CONDITIONS = [
    "Thunderstorm",
    "Heavy Rain",
    "Heavy Rain Showers",
]