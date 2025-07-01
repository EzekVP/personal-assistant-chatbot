from fastapi import FastAPI, Request, Query
from typing import Dict
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

OPENWEATHERMAP_API_KEY: str | None = os.getenv("OPENWEATHERMAP_API_KEY")


@app.get("/weather")
def get_weather(location: str = Query(..., min_length=2)) -> Dict[str, str]:
    if not OPENWEATHERMAP_API_KEY:
         return {"error": "API key not configured"}

    api_url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    )

    try:
        res = requests.get(api_url, timeout=5)

         # 🔍 Debug output to see real error details
        print("DEBUG OpenWeather status:", res.status_code)
        print("DEBUG OpenWeather response:", res.text)
        
        if res.status_code != 200:
            return {"error": "Could not retrieve weather info"}

        data = res.json()
        weather = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        forecast = (
            f"Weather in {location}:\n"
            f"- {weather}\n"
            f"- Temperature: {temp}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind: {wind} m/s"
        )

        return {"forecast": forecast}

    except Exception as e:
        return {"error": str(e)}
