import sqlite3
from datetime import datetime

DB_NAME = "weather_alerts.db"


def get_today_alerts():
    today = datetime.now().date().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, title, message
        FROM alerts
        WHERE DATE(timestamp) = ?
        ORDER BY timestamp ASC
        """,
        (today,)
    )

    alerts = cursor.fetchall()
    conn.close()

    return alerts


def show_daily_summary():
    alerts = get_today_alerts()

    print("=" * 40)
    print("Daily Weather Summary")
    print("=" * 40)
    print(f"Alerts today: {len(alerts)}")
    print()

    if not alerts:
        print("No alerts recorded today.")
        return

    for timestamp, title, message in alerts:
        time_only = timestamp.split("T")[1]

        print(f"{time_only} - {title}")
        print(message)
        print("-" * 40)


if __name__ == "__main__":
    show_daily_summary()