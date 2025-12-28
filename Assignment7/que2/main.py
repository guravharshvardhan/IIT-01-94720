from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
import streamlit as st 
import requests
#Create a Streamlit application that takes a city name as input from the user.
#Fetch the current weather using a Weather API and use an LLM to explain the weather conditions in simple English.

load_dotenv()

st.title("WEATHER APPLICATION")

api_key=os.getenv("OPENWEATHER_API_KEY")
api_key1 = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    api_key=api_key1,
    base_url="https://api.groq.com/openai/v1"
)

city=st.chat_input("Enter city name")

if st.button("Get Weather"):
    url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

    response = requests.get(url)

    if response.status_code !=200:
        st.error("city not found")
    else:
        data = response.json()


        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        wind = data["wind"]["speed"]

        st.subheader(" Current Weather Data")
        st.write(f" Temperature: {temp} °C")
        st.write(f" Humidity: {humidity}%")
        st.write(f" Wind Speed: {wind} m/s")
        st.write(f" Condition: {condition}")


        prompt = f"""
The current weather in {city} is:
- Temperature: {temp} °C
- Humidity: {humidity}%
- Wind speed: {wind} m/s
- Condition: {condition}

Explain this weather in very simple English
so that a normal person can easily understand it.
"""
        with st.spinner("Explaining weather..."):
                explanation = llm.invoke(prompt).content

        st.subheader(" Simple Explanation")
        st.success(explanation)