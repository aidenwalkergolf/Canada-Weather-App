import streamlit as st
from utils import get_unit_label
from datetime import datetime

def display_main_ui(data, user_city_data, units, theme):
    if st.session_state.forecast_days == 1:
        # 1-day layout: individual cards
        cols = st.columns(7)
        for i, (loc, weather) in enumerate(data.items()):
            with cols[i % 7]:
                _display_card(loc, weather, units, theme)
    else:
        # 7-day forecast: one row per city
        for loc in data:
            st.markdown(f"### {loc}")
            forecast = user_city_data.get(loc)
            if forecast:
                _display_forecast_row(forecast, units,theme)
            else:
                st.warning("Forecast unavailable.")

def _display_card(location, weather, units, theme):
    bg_color = "#1e1e1e" if theme == "dark" else "#f0f0f0"
    text_color = "#ffffff" if theme == "dark" else "#000000"
    icon_bg = "#bbbbbb" if theme == "dark" else "#bbbbbb"

    try:
        icon_code = weather["weather"][0]["icon"]
        description = weather["weather"][0]["description"].title()
        temp = round(weather["main"]["temp"])
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]
    except KeyError:
        st.warning("Weather data unavailable.")
        return

    st.markdown(
        f"""
        <div style="
            background-color: {bg_color};
            color: {text_color};
            padding: 15px;
            border-radius: 12px;
            font-size: 13px;
            line-height: 1.4;
            height: 260px;
            text-align: center;
            margin-bottom: 20px;
        ">
            <p style="margin-bottom: 8px; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: center; font-weight: bold;">{location}</p>
            <div style="background:{icon_bg}; padding:5px; border-radius:8px; display:inline-block;">
                <img src="http://openweathermap.org/img/wn/{icon_code}@2x.png" width="40"/>
            </div>
            <p style="margin: 5px 0;">{description}</p>
            <p><strong>Temp:</strong> {temp} {get_unit_label(units)}</p>
            <p><strong>Humidity:</strong> {humidity}%</p>
            <p><strong>Wind:</strong> {wind} m/s</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def _display_forecast_row(forecast_data, units, theme):
    bg_color = "#1e1e1e" if theme == "dark" else "#f0f0f0"
    text_color = "#ffffff" if theme == "dark" else "#000000"
    icon_bg = "#bbbbbb" if theme == "dark" else "#bbbbbb"

    days_to_show = min(7, len(forecast_data["daily"]))
    cols = st.columns(days_to_show)

    for i in range(days_to_show):
        day = forecast_data["daily"][i]
        icon_code = day["weather"][0]["icon"]
        description = day["weather"][0]["description"].title()
        temp = round(day["temp"]["day"])
        wind = day["wind_speed"]
        humidity = day.get("humidity", "-")
        weekday = datetime.fromtimestamp(day["dt"]).strftime('%A')

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    color: {text_color};
                    padding: 15px;
                    border-radius: 12px;
                    font-size: 13px;
                    line-height: 1.4;
                    height: 260px;
                    text-align: center;
                    margin-bottom: 20px;
                ">
                    <p style="margin: 0 auto 8px auto; font-size: 13px; font-weight: bold; text-align: center;">{weekday}</p>
                    <div style="background:{icon_bg}; padding:5px; border-radius:8px; display:inline-block;">
                        <img src="http://openweathermap.org/img/wn/{icon_code}@2x.png" width="40"/>
                    </div>
                    <p style="margin: 5px 0;">{description}</p>
                    <p><strong>Temp:</strong> {temp} {get_unit_label(units)}</p>
                    <p><strong>Humidity:</strong> {humidity}%</p>
                    <p><strong>Wind:</strong> {wind} m/s</p>
                </div>
                """,
                unsafe_allow_html=True
            )
