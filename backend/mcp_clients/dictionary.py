import requests
from typing import Dict

MCP_DICTIONARY_URL = "http://localhost:9004/define"

def send_to_dictionary_mcp(word: str) -> Dict[str, str]:
    try:
        res = requests.post(MCP_DICTIONARY_URL, json={"word": word}, timeout=5)
        return res.json()
    except Exception as e:
        return {"error": str(e)}
