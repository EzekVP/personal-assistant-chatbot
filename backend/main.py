from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import Dict, Any
from mcp_clients.reminders import send_to_reminder_mcp
from mcp_clients.weather import send_to_weather_mcp
from mcp_clients.finance import send_to_finance_mcp
from mcp_clients.wiki import send_to_wiki_mcp
import requests

app = FastAPI()

# -------------------- Root Health Check --------------------
@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Personal Assistant Chatbot Backend is running"}

# -------------------- Reminder Endpoints --------------------
@app.post("/reminder")
async def reminder_endpoint(request: Request) -> JSONResponse:
    try:
        body: Dict[str, Any] = await request.json()

        # Validation
        if "task" not in body or "time" not in body:
            return JSONResponse(status_code=400, content={"error": "Missing 'task' or 'time'"})
        if not isinstance(body["task"], str) or not isinstance(body["time"], str):
            return JSONResponse(status_code=400, content={"error": "'task' and 'time' must be strings"})

        response = send_to_reminder_mcp(body)
        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Something went wrong", "details": str(e)})

@app.get("/reminders")
def get_reminders():
    try:
        res = requests.get("http://localhost:9001/reminders")
        return res.json()
    except Exception as e:
        return {"error": str(e)}

@app.delete("/reminder/{reminder_id}")
def delete_reminder(reminder_id: int):
    try:
        res = requests.delete(f"http://localhost:9001/reminders/{reminder_id}")
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 404:
            raise HTTPException(status_code=404, detail="Task not found")
        else:
            raise HTTPException(status_code=500, detail="Unexpected error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/reminder/{reminder_id}")
def update_reminder(reminder_id: int, data: dict = Body(...)):
    try:
        res = requests.put(f"http://localhost:9001/reminders/{reminder_id}", json=data)
        if res.status_code == 200:
            return res.json()
        elif res.status_code == 404:
            raise HTTPException(status_code=404, detail="Reminder not found")
        else:
            raise HTTPException(status_code=500, detail="Unexpected error")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------- Weather Endpoint --------------------
@app.post("/weather")
async def weather_endpoint(request: Request) -> Dict[str, str]:
    body = await request.json()
    location = body.get("location")

    if not location or not isinstance(location, str):
        return {"error": "Missing or invalid 'location'"}

    return send_to_weather_mcp(location)

# -------------------- Finance Endpoint --------------------
@app.post("/finance")
async def finance_endpoint(request: Request) -> Dict[str, str]:
    body: Dict[str, Any] = await request.json()

    amount = body.get("amount")
    from_currency = body.get("from_currency")
    to_currency = body.get("to_currency")

    # Validation
    if not all([amount, from_currency, to_currency]):
        return {"error": "Missing required parameters"}

    payload = {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
    }

    return send_to_finance_mcp(payload)

# -------------------- Wikipaedia Endpoint --------------------

# POST /wiki — Forward query to Wikipedia MCP server
@app.post("/wiki")
async def wiki_endpoint(request: Request) -> Dict[str, str]:
    body: Dict[str, Any] = await request.json()
    query = body.get("query")

    if not query or not isinstance(query, str):
        return {"error": "Missing or invalid 'query'"}

    return send_to_wiki_mcp(query)