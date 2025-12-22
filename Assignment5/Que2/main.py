import os
import requests
from dotenv import load_dotenv 
import time
import json

load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

headers={
    "Authorization":f"Bearer {api_key}",
    "content-type":"application/json"
}

print("__groq api__")
while True:
    user_input=input("ask anything")

    if user_input=="exit":
        break

    req_data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            { "role": "user", "content": user_input }
        ],
    }

    time_1=time.perf_counter()
    response=requests.post(url, data=json.dumps(req_data),headers=headers)
    res=response.json()
    time_2=time.perf_counter()
    print("GROQ_AI",res["choices"][0]["message"]["content"])

    load_dotenv()
    api_key=os.getenv("GEMINI_API_KEY")
    url="https://generativelanguage.googleapis.com/v1/"

    headers={
        "Authorization":f"bearer{api_key}",
        "content-type":"application/json"
    }
print("__gemini api___")
while True:
    user_input=("ask anything")
    
    if user_input=="exit":
                break
    req_data = {
        "messages": [
            { "role": "user", "content": user_input }
        ],
    }

    time_3=time.perf_counter()
    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    res=response.json()
    time_4=time.perf_counter()
    print(res)
    #print("Geini_AI:",res["choices"][0]["message"]["content"])
    print(f"Time for Gemini is:{time_4-time_3}")

