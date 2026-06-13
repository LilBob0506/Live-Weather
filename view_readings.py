import sqlite3

DB_NAME = "weather_alerts.db"


def view_readings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, temperature, condition, rain, precipitation, wind_speed
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 10
    """)

    readings = cursor.fetchall()
    conn.close()

    if not readings:
        print("No weather readings found.")
        return

    for reading in readings:
        timestamp, temperature, condition, rain, precipitation, wind_speed = reading

        print("-" * 50)
        print(f"Time: {timestamp}")
        print(f"Temperature: {temperature}°F")
        print(f"Condition: {condition}")
        print(f"Rain: {rain}")
        print(f"Precipitation: {precipitation}")
        print(f"Wind Speed: {wind_speed} mph")


if __name__ == "__main__":
    view_readings()