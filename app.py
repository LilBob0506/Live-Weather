import sqlite3
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from datetime import datetime
from weather import get_weather
from database import save_weather_reading
from datetime import datetime
from config import CITY, STATE

DB_NAME = "weather_alerts.db"

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def format_timestamp(timestamp):
    if not timestamp:
        return ""

    dt = datetime.fromisoformat(timestamp)

    return dt.strftime("%m/%d/%Y %I:%M %p").lstrip("0")


def get_weather_history_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            temperature,
            condition,
            wind_speed,
            precipitation
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 200
    """)

    rows = cursor.fetchall()
    conn.close()

    readings = []

    for row in rows:
        readings.append({
            "timestamp": format_timestamp(row[0]),
            "temperature": row[1],
            "condition": row[2],
            "wind_speed": row[3],
            "precipitation": row[4],
        })

    return readings


def get_all_alerts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, title, message
        FROM alerts
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    alerts = []

    for timestamp, title, message in rows:
        alerts.append({
            "timestamp": format_timestamp(timestamp),
            "title": title,
            "message": message,
            "severity": get_alert_severity(message)
        })

    return alerts


def get_status_text(weather_stale):
    if weather_stale:
        return "Inactive or outdated"

    return "Active"


def get_forecast_chart_data(forecast):
    labels = []
    temperatures = []
    rain_chances = []

    for row in forecast:
        dt = datetime.fromisoformat(row[0])

        labels.append(
            dt.strftime("%I %p").lstrip("0")
        )

        temperatures.append(row[1])
        rain_chances.append(row[2])

    return labels, temperatures, rain_chances


def get_alert_severity(message):
    message = message.lower()

    severe_keywords = [
        "thunderstorm",
        "heavy rain",
        "severe weather"
    ]

    warning_keywords = [
        "wind increased",
        "rain has started"
    ]

    if any(word in message for word in severe_keywords):
        return "severe"

    if any(word in message for word in warning_keywords):
        return "warning"

    return "info"


def get_weather_icon(condition):
    condition = condition.lower()

    if "clear" in condition:
        return "☀️"
    if "cloudy" in condition or "overcast" in condition:
        return "☁️"
    if "rain" in condition or "drizzle" in condition:
        return "🌧️"
    if "thunderstorm" in condition:
        return "⛈️"
    if "snow" in condition:
        return "❄️"
    if "fog" in condition:
        return "🌫️"

    return "🌡️"


def get_saved_forecast():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            forecast_time,
            temperature,
            precipitation_probability,
            condition
        FROM forecasts
        ORDER BY forecast_time
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_last_update():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None


def get_weather_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            MAX(temperature),
            MIN(temperature),
            AVG(temperature),
            MAX(wind_speed)
        FROM weather_readings
        WHERE DATE(timestamp) = DATE('now', 'localtime')
    """)

    result = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE DATE(timestamp) = DATE('now', 'localtime')
    """)

    alert_count = cursor.fetchone()[0]

    conn.close()

    return {
        "high_temp": round(result[0], 1) if result[0] else None,
        "low_temp": round(result[1], 1) if result[1] else None,
        "avg_temp": round(result[2], 1) if result[2] else None,
        "max_wind": round(result[3], 1) if result[3] else None,
        "alert_count": alert_count,
    }


def get_weather_stats():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            MAX(temperature),
            MIN(temperature),
            AVG(temperature),
            MAX(wind_speed)
        FROM weather_readings
        WHERE DATE(timestamp) = DATE('now', 'localtime')
    """)

    result = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM alerts
        WHERE DATE(timestamp) = DATE('now', 'localtime')
    """)

    alert_count = cursor.fetchone()[0]

    conn.close()

    return {
        "high_temp": round(result[0], 1) if result[0] else None,
        "low_temp": round(result[1], 1) if result[1] else None,
        "avg_temp": round(result[2], 1) if result[2] else None,
        "max_wind": round(result[3], 1) if result[3] else None,
        "alert_count": alert_count,
    }


def is_weather_stale(weather):
    if not weather:
        return True

    timestamp = datetime.fromisoformat(weather[0])
    now = datetime.now()

    minutes_old = (now - timestamp).total_seconds() / 60

    return minutes_old > 10

def get_weather_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, temperature, wind_speed, precipitation
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()
    conn.close()

    rows.reverse()

    labels = []
    temperatures = []
    wind_speeds = []
    precipitations = []

    for row in rows:
        dt = datetime.fromisoformat(row[0])

        labels.append(
            dt.strftime("%I:%M %p").lstrip("0")
        )

        temperatures.append(row[1])
        wind_speeds.append(row[2])
        precipitations.append(row[3])

    return labels, temperatures, wind_speeds, precipitations


def get_latest_weather():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, temperature, condition, rain, precipitation, wind_speed
        FROM weather_readings
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    return row


def get_recent_alerts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, title, message
        FROM alerts
        ORDER BY id DESC
        LIMIT 5
    """)

    rows = cursor.fetchall()
    conn.close()

    alerts = []

    for timestamp, title, message in rows:
        alerts.append({
            "timestamp": format_timestamp(timestamp),
            "title": title,
            "message": message,
            "severity": get_alert_severity(message)
        })

    return alerts


@app.get("/")
def dashboard(request: Request):
    latest_weather = get_latest_weather()
    last_updated = format_timestamp(latest_weather[0]) if latest_weather else ""

    weather_icon = get_weather_icon(latest_weather[2]) if latest_weather else "🌡️"
    recent_alerts = get_recent_alerts()

    labels, temperatures, wind_speeds, precipitations = get_weather_history()
    weather_stale = is_weather_stale(latest_weather)
    stats = get_weather_stats()
    forecast = get_saved_forecast()
    forecast_labels, forecast_temps, forecast_rain = get_forecast_chart_data(forecast)
    last_update = get_last_update()
    status_text = get_status_text(weather_stale)

    formatted_forecast = []

    for row in forecast:
        dt = datetime.fromisoformat(row[0])

        formatted_forecast.append({
            "time": dt.strftime("%I:%M %p").lstrip("0"),
            "temp": row[1],
            "rain": row[2],
            "condition": row[3]
        })

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "weather": latest_weather,
            "alerts": recent_alerts,
            "labels": labels,
            "temperatures": temperatures,
            "wind_speeds": wind_speeds,
            "precipitations": precipitations,
            "weather_stale": weather_stale,
            "stats": stats,
            "forecast": formatted_forecast,
            "last_update": last_update,
            "weather_icon": weather_icon,
            "forecast_labels": forecast_labels,
            "forecast_temps": forecast_temps,
            "forecast_rain": forecast_rain,
            "city": CITY,
            "state": STATE,
            "status_text": status_text,
            "last_updated": last_updated,
        }
    )

@app.get("/alerts")
def alert_history(request: Request):
    alerts = get_all_alerts()

    return templates.TemplateResponse(
        request=request,
        name="alerts.html",
        context={
            "alerts": alerts
        }
    )

@app.get("/history")
def weather_history(request: Request):
    readings = get_weather_history_table()

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "readings": readings
        }
    )

@app.get("/refresh-weather")
def refresh_weather():
    current_weather = get_weather()
    save_weather_reading(current_weather)

    return RedirectResponse(
        url="/",
        status_code=303
    )
