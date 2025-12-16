import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="Weather App")

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Fake authentication
        if username == password and username != "":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid login (username & password must be same)")

# ---------------- WEATHER PAGE ----------------
else:
    st.title("🌤 Weather Information")

    city = st.text_input("Enter city name")

    if st.button("Get Weather"):
        if not API_KEY:
            st.error("API key not found. Check .env file")
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                st.error(data.get("message", "Error fetching weather"))
            else:
                st.success(f"Weather in {city}")
                st.write(f"🌡 Temperature: {data['main']['temp']} °C")
                st.write(f"💧 Humidity: {data['main']['humidity']} %")
                st.write(f"☁ Condition: {data['weather'][0]['description']}")

    # ---------------- LOGOUT ----------------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.success("Thanks for using the app 👋")
        st.stop()
