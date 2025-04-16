import streamlit as st
from layout import display_main_ui
from weather_data import get_all_weather_data, get_forecast_by_coords
from utils import switch_units, get_unit_label, get_city_coordinates

# Streamlit page setup
st.set_page_config(page_title="Canada Weather App", layout="wide")
st.title("Canada Weather App")

# Session state defaults
if 'unit' not in st.session_state:
    st.session_state.unit = 'metric'

if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

if 'forecast_days' not in st.session_state:
    st.session_state.forecast_days = 1

# Top controls: unit toggle, theme toggle, forecast range
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Toggle Units"):
        st.session_state.unit = switch_units(st.session_state.unit)
    st.write(f"Current Units: {get_unit_label(st.session_state.unit)}")

with col2:
    if st.button("Toggle Theme"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.write(f"Current Theme: {st.session_state.theme.capitalize()} Mode")

with col3:
    st.session_state.forecast_days = st.selectbox("Forecast Range", [1, 7], index=0)

# Load weather and forecast data
user_city_data = {}
with st.spinner("Loading weather data..."):
    try:
        weather_data = get_all_weather_data(st.session_state.unit)

        if st.session_state.forecast_days > 1:
            # Get forecast for all cities
            for loc, weather in weather_data.items():
                if "coord" in weather:
                    lat = weather["coord"]["lat"]
                    lon = weather["coord"]["lon"]
                    forecast = get_forecast_by_coords(lat, lon, st.session_state.unit, st.session_state.forecast_days)
                    user_city_data[loc] = forecast
        else:
            user_city_data = None

    except Exception as e:
        st.error(f"Error retrieving weather data: {e}")
        weather_data = {}
        user_city_data = None

# Render the UI
display_main_ui(weather_data, user_city_data, st.session_state.unit, st.session_state.theme)
