from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Body
from typing import Dict, Any
from mcp_clients.reminders import send_to_reminder_mcp
from mcp_clients.weather import send_to_weather_mcp
import requests

app = FastAPI()

#  Health check
@app.get("/")
def read_root() -> Dict[str, str]:
    return {"message": "Personal Assistant Chatbot Backend is running"}

#  Create new reminder
@app.post("/reminder")
async def reminder_endpoint(request: Request) -> JSONResponse:
    try:
        body: Dict[str, Any] = await request.json()

        # Validation
        if "task" not in body or "time" not in body:
            return JSONResponse(status_code=400, content={"error": "Missing 'task' or 'time'"})

        if not isinstance(body["task"], str) or not isinstance(body["time"], str):
            return JSONResponse(status_code=400, content={"error": "'task' and 'time' must be strings"})

        # Forward to MCP
        response = send_to_reminder_mcp(body)
        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Something went wrong", "details": str(e)})

#  View all reminders
@app.get("/reminders")
def get_reminders():
    try:
        res = requests.get("http://localhost:9001/reminders")
        return res.json()
    except Exception as e:
        return {"error": str(e)}

#  Delete a reminder
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

# PUT /reminder/{reminder_id} — Forward edit to MCP
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
    
# POST /weather — Forward weather query to MCP
@app.post("/weather")
async def weather_endpoint(request: Request) -> Dict[str, str]:
    body = await request.json()
    location = body.get("location")

    if not location or not isinstance(location, str):
        return {"error": "Missing or invalid 'location'"}

    response = send_to_weather_mcp(location)
    return response
