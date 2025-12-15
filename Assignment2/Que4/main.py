from dotenv import load_dotenv
import os
import requests
load_dotenv()

api_key = os.getenv("API_KEY")
city = input("Enetr the City name : ")

url=f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}&units=metric"

response = requests.get(url)

weather = response.json()

print(weather)
