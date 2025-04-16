import requests
import os

API_KEY = "ec63d2b7897cf7b00ce7be57fb24f1b8"

CITIES = [
    ("Toronto", "ON"),
    ("Montreal", "QC"),
    ("Vancouver", "BC"),
    ("Calgary", "AB"),
    ("Winnipeg", "MB"),
    ("Halifax", "NS"),
    ("St. John's", "NL"),
    ("Fredericton", "NB"),
    ("Charlottetown", "PE"),
    ("Regina", "SK"),
    ("Whitehorse", "YT"),
    ("Yellowknife", "NT"),
    ("Iqaluit", "NU")
]

def get_weather(city, units):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},CA&appid={API_KEY}&units={units}"
    return requests.get(url).json()

def get_all_weather_data(units):
    return {f"{city}, {prov}": get_weather(city, units) for city, prov in CITIES}

def get_forecast_by_coords(lat, lon, units='metric', days=7):
    url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,hourly&units={units}&appid={API_KEY}"
    )
    response = requests.get(url)
    return response.json()
