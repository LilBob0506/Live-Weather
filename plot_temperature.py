import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

DB_NAME = "weather_alerts.db"


def plot_temperature():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, temperature
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 100
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No weather data found.")
        return

    rows.reverse()

    timestamps = []
    temperatures = []

    for timestamp, temperature in rows:
        timestamps.append(
            datetime.fromisoformat(timestamp)
        )
        temperatures.append(temperature)

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, temperatures)

    plt.title("Temperature History")
    plt.xlabel("Time")
    plt.ylabel("Temperature (°F)")

    plt.tight_layout()

    plt.savefig("temperature_history.png")

    print("Saved graph as temperature_history.png")


if __name__ == "__main__":
    plot_temperature()