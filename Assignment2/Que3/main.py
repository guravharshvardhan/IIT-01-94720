import requests
import json
import pandas as pd
from pathlib import Path

API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_data(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()

def save_json(data, filepath):
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_csv(data, filepath):
    df = pd.DataFrame(data)
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)

def main():
    data = fetch_data(API_URL)
    save_json(data, "output/posts.json")
    save_csv(data, "output/posts.csv")
    print("Files saved in output folder.")

if __name__ == "__main__":
    main()
