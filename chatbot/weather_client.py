import requests
from typing import Optional

BASE_URL: str = "http://localhost:9002"

def get_weather(location: str) -> Optional[str]:
    try:
        res = requests.get(f"{BASE_URL}/weather", params={"location": location}, timeout=5)
        data = res.json()

        if res.status_code == 200:
            return data.get("forecast", "Weather info unavailable.")
        else:
            return f"Sorry, couldn't fetch weather: {data.get('error', 'Unknown error')}"

    except Exception as e:
        return f"Error: {str(e)}"
