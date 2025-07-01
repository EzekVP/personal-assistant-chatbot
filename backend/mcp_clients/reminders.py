import requests
from typing import Dict, Any

def send_to_reminder_mcp(payload: Dict[str, Any]) -> Dict[str, Any]:
    # url for my reminder mcp server   
    mcp_url = "http://localhost:9001/mcp"

    try:
        response = requests.post(mcp_url, json=payload)
        return response.json()
    except Exception as e:
        return {"error" : str(e)}
