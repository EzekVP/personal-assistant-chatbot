import requests

BASE_URL = "http://localhost:8000"

def get_wiki_summary(query: str) -> str:
    try:
        res = requests.post(f"{BASE_URL}/wiki", json={"query": query}, timeout=20)
        data = res.json()
        if "summary" in data:
            return data["summary"]
        return f"Sorry, couldn't find anything for '{query}'."
    except Exception as e:
        return f"Error: {str(e)}"
