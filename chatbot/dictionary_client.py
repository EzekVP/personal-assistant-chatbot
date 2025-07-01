import requests
from typing import Optional

BASE_URL = "http://localhost:8000"

def get_definition(word: str) -> Optional[str]:
    try:
        res = requests.post(
            f"{BASE_URL}/dictionary",
            json={"word": word},
            timeout=5
        )

        if res.status_code == 200:
            data = res.json()
            if "definition" in data:
                return f"{word.capitalize()}: {data['definition']}"
            elif "error" in data:
                return f"Sorry, couldn't find meaning for '{word}'."
        return "Failed to get dictionary data."
    
    except Exception as e:
        return f"Error: {str(e)}"
