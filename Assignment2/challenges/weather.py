from dotenv import load_dotenv
import os
from utils import get_weather

load_dotenv()  # loads .env file

def get_Whea():
    data = get_weather(city)
    # print(f"Full Data : \n {data}")
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    print("\n--- Weather Report ---")
    print(f"Temperature: {temp} °C")
    print(f"Humidity: {humidity} %")

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_Whea()