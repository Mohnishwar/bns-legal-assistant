import requests
import json

url = "https://api.parse.bot/scraper/f98e7b18-d990-4cec-8087-0dc00d0bbe1e/run"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": "84242bee-1ef7-45b6-a784-329b3bdd3451"  # replace with your actual API key
}

payload = {
    "count": 3
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()

    # Save to a JSON file
    with open("BNS.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("✅ JSON saved to output.json")
else:
    print(f"Error: {response.status_code} - {response.text}")



