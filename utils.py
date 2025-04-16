import requests
import os

def switch_units(current_unit):
    return "imperial" if current_unit == "metric" else "metric"

def get_unit_label(unit):
    return "°C" if unit == "metric" else "°F"

def get_city_coordinates(city_name):
    API_KEY = os.getenv("OPENWEATHER_API_KEY") or "YOUR_API_KEY_HERE"
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},CA&limit=1&appid={API_KEY}"
    response = requests.get(url).json()
    if not response:
        raise ValueError("City not found.")
    return response[0]['lat'], response[0]['lon']
