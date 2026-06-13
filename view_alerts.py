import sqlite3

DB_NAME = "weather_alerts.db"


def view_alerts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, title, message
        FROM alerts
        ORDER BY id DESC
        LIMIT 10
    """)

    alerts = cursor.fetchall()

    conn.close()

    if not alerts:
        print("No alerts found.")
        return

    for alert in alerts:
        alert_id, timestamp, title, message = alert

        print("-" * 40)
        print(f"ID: {alert_id}")
        print(f"Time: {timestamp}")
        print(f"Title: {title}")
        print(f"Message: {message}")


if __name__ == "__main__":
    view_alerts()