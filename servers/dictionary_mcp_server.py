from fastapi import FastAPI, Request
from typing import Dict
import requests

app = FastAPI()

DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

@app.post("/define")
async def define_word(request: Request) -> Dict[str, str]:
    try:
        body = await request.json()
        word = body.get("word")

        if not word or not isinstance(word, str):
            return {"error": "Invalid or missing 'word'"}

        res = requests.get(f"{DICTIONARY_API_URL}{word}", timeout=5)

        if res.status_code != 200:
            return {"error": f"Couldn't find definition for '{word}'"}

        data = res.json()[0]
        meanings = data.get("meanings", [])
        if not meanings:
            return {"error": "No meanings found."}

        # Take first available meaning and definition
        part_of_speech = meanings[0].get("partOfSpeech", "unknown")
        definition = meanings[0]["definitions"][0].get("definition", "No definition available")
        example = meanings[0]["definitions"][0].get("example", "No example available")

        return {
            "definition": f"{word} ({part_of_speech}): {definition}",
            "example": f"Example: {example}"
        }

    except Exception as e:
        return {"error": str(e)}
