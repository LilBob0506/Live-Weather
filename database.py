import sqlite3
from datetime import datetime

DB_NAME = "weather_alerts.db"


def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forecast_time TEXT NOT NULL,
            temperature REAL NOT NULL,
            precipitation_probability REAL NOT NULL,
            condition TEXT NOT NULL,
            saved_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_forecast(forecast):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM forecasts")

    for item in forecast:
        cursor.execute(
            """
            INSERT INTO forecasts (
                forecast_time,
                temperature,
                precipitation_probability,
                condition,
                saved_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                item["time"],
                item["temperature"],
                item["precipitation_probability"],
                item["condition"],
                datetime.now().isoformat(timespec="seconds")
            )
        )

    conn.commit()
    conn.close()


def save_alert(title, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO alerts (timestamp, title, message)
        VALUES (?, ?, ?)
        """,
        (datetime.now().isoformat(timespec="seconds"), title, message)
    )

    conn.commit()
    conn.close()


def save_weather_reading(weather):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            condition TEXT NOT NULL,
            rain REAL NOT NULL,
            precipitation REAL NOT NULL,
            wind_speed REAL NOT NULL
        )
    """)

    cursor.execute(
        """
        INSERT INTO weather_readings (
            timestamp,
            temperature,
            condition,
            rain,
            precipitation,
            wind_speed
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().isoformat(timespec="seconds"),
            weather["temperature"],
            weather["condition"],
            weather["rain"],
            weather["precipitation"],
            weather["wind_speed"],
        )
    )

    conn.commit()
    conn.close()