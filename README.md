# LiveWeather

A Python-based weather monitoring application that tracks live weather conditions, stores historical weather data, generates desktop notifications for significant weather changes, and provides a web dashboard for visualization and forecasting.

## Features

### Weather Monitoring

* Real-time weather monitoring using Open-Meteo API
* Automatic weather polling at configurable intervals
* City-based location configuration

### Alerts & Notifications

* Desktop notifications for weather changes
* Rain detection alerts
* Wind increase alerts
* Severe weather detection
* Alert severity classification

### Data Storage

* SQLite database for historical weather data
* Alert history storage
* Forecast data storage
* Daily weather statistics

### Dashboard

* FastAPI web dashboard
* Current weather summary
* Temperature history chart
* Wind speed history chart
* Precipitation history chart
* 24-hour forecast table
* Forecast temperature chart
* Forecast rain probability chart
* Service status monitoring

### Historical Data

* Alert history page
* Weather history page
* Daily statistics
* Weather trend visualization

## Tech Stack

### Backend

* Python
* FastAPI
* SQLite
* Open-Meteo API

### Frontend

* HTML
* CSS
* Jinja2 Templates
* Chart.js

### Notifications

* macOS Notification Center (AppleScript)

## Project Structure

```text
liveweather/
├── app.py
├── weather_monitor.py
├── weather.py
├── database.py
├── notifier.py
├── logger.py
├── config.py
├── weather_alerts.db
├── logs/
├── templates/
│   ├── dashboard.html
│   ├── alerts.html
│   └── history.html
└── static/
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd liveweather
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the weather monitoring service:

```bash
python weather_monitor.py
```

In a separate terminal:

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Quick Start

Create a `.env` file:

```env
CITY=YourCity
STATE=YourState
COUNTRY=YourCountry
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the weather collector:

```bash
python weather_monitor.py
```

In a separate terminal start the dashboard:

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```


## Future Improvements

* Weather radar integration
* Multi-location monitoring
* User authentication
* Mobile-friendly dashboard
* Docker deployment
* Cloud hosting
* Email/SMS notifications
* Advanced filtering and search
