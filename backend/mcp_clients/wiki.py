import requests
from typing import Dict

BASE_URL = "http://localhost:9003/summary"

def send_to_wiki_mcp(query: str) -> Dict[str, str]:
    try:
        res = requests.post(BASE_URL, json={"query": query}, timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
