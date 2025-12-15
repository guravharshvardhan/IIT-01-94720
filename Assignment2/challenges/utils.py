
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        "https://api.openweathermap.org/data/2.5/weather"f"?q={city}&appid={api_key}&units=metric"
    )

    response = requests.get(url, timeout=10)
    return response.json()
