import time
from weather import get_weather, get_forecast
from notifier import send_notification
from config import (
    TEMP_CHANGE_THRESHOLD,
    WIND_CHANGE_THRESHOLD,
    SEVERE_CONDITIONS,
    CHECK_INTERVAL,
)
from database import initialize_database, save_alert, save_weather_reading, save_forecast
from logger import logger


def weather_changed(old, new):
    messages = []

    temp_diff = abs(new["temperature"] - old["temperature"])

    if temp_diff >= TEMP_CHANGE_THRESHOLD:
        messages.append(
            f"Temperature changed from {old['temperature']}°F to {new['temperature']}°F"
        )

    if old["rain"] == 0 and new["rain"] > 0:
        messages.append("Rain has started.")

    if (new["wind_speed"] - old["wind_speed"]>= WIND_CHANGE_THRESHOLD):
        messages.append(
            f"Wind increased from {old['wind_speed']} mph to {new['wind_speed']} mph"
        )
    
    if old["condition"] != new["condition"]:
        messages.append(
            f"Weather changed from {old['condition']} to {new['condition']}"
        )
    
    if (
        new["condition"] in SEVERE_CONDITIONS
        and old["condition"] != new["condition"]
    ):
        messages.append(
            f"Severe weather detected: {new['condition']}"
        )

    return messages


def main():
    initialize_database()

    previous_weather = get_weather()
    save_weather_reading(previous_weather)

    print("Starting Weather:", previous_weather)

    send_notification("Weather Notifier", "Weather monitoring started.")

    while True:
        time.sleep(CHECK_INTERVAL)

        current_weather = get_weather()
        save_weather_reading(current_weather)
        logger.info(f"Weather Reading: {current_weather}")

        forecast = get_forecast()
        save_forecast(forecast)

        print("Current Weather:", current_weather)

        changes = weather_changed(previous_weather, current_weather)

        if changes:
            alert_message = "\n".join(changes)
            logger.warning(alert_message)

            print("Changes detected:", changes)

            send_notification(
                "Weather Change Detected",
                alert_message
            )

            save_alert(
                "Weather Change Detected",
                alert_message
            )

        previous_weather = current_weather
        
        forecast = get_forecast()
        save_forecast(forecast)


if __name__ == "__main__":
    main()