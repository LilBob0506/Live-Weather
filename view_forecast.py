import sqlite3

DB_NAME = "weather_alerts.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
    SELECT forecast_time, temperature, precipitation_probability, condition
    FROM forecasts
    ORDER BY forecast_time
    LIMIT 10
""")

rows = cursor.fetchall()

conn.close()

for row in rows:
    print(row)