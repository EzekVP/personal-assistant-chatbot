from fastapi import FastAPI, Request
from typing import Dict
import wikipedia

app = FastAPI()

@app.post("/summary")  
async def get_wiki_summary(request: Request) -> Dict[str, str]:
    body = await request.json()
    query = body.get("query")

    if not query or not isinstance(query, str):
        return {"error": "Missing or invalid query"}

    try:
        summary = wikipedia.summary(query, sentences=3)
        return {"summary": summary}
    except wikipedia.exceptions.DisambiguationError as e:
        return {"error": f"Query is ambiguous. Try one of: {e.options[:3]}"}
    except wikipedia.exceptions.PageError:
        return {"error": "No Wikipedia page found for that topic"}
    except Exception as e:
        return {"error": str(e)}
