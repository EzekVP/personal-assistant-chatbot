import requests
from typing import Dict, Any

BASE_URL = "http://localhost:9003/mcp"

def send_to_finance_mcp(payload: Dict[str, Any]) -> Dict[str, str]:
    try:
        res = requests.post(BASE_URL, json=payload, timeout=5)
        print("DEBUG Finance MCP response:", res.status_code, res.text)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
