import requests
from typing import Dict

def send_to_weather_mcp(location: str) -> Dict[str, str]:
    
    mcp_url = "http://localhost:9002/weather"
    try:
        res = requests.get(mcp_url, params={"location": location}, timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
