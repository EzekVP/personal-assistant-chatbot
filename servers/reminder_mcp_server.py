from fastapi import FastAPI, Request
from typing import Dict, List, Any
from fastapi import HTTPException
# from fastapi import Path
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from plyer import notification
import json
import os

app = FastAPI()

REMINDER_FILE = "reminders.json"

#  Helper to load existing reminders
def load_reminders() -> List[Dict[str, Any]]:
    if not os.path.exists(REMINDER_FILE):
        return []
    try:
        with open(REMINDER_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


#  Helper to save updated reminders
def save_reminders(reminders: List[Dict[str, Any]]) -> None:
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)

#  POST /mcp → Save reminder with ID
@app.post("/mcp")
async def handle_mcp(request: Request) -> Dict[str, Any]:
    body = await request.json()
    task = body.get("task")
    time = body.get("time")

    if not task or not time:
        return {"error": "Missing 'task' or 'time'"}

    reminders = load_reminders()
    next_id = 1 if not reminders else reminders[-1]["id"] + 1

    new_reminder = {
        "id": next_id,
        "task": task,
        "time": time
    }

    reminders.append(new_reminder)
    save_reminders(reminders)

    return {"status": "sure why not \U0001F603 ", "reminder": new_reminder}

#  GET /reminders → Return all saved reminders
@app.get("/reminders")
def get_reminders() -> List[Dict[str, Any]]:
    return load_reminders()


#  DELETE /reminders/{id} — Delete a reminder by ID
@app.delete("/reminders/{reminder_id}")
def delete_reminder(reminder_id: int):
    reminders = load_reminders()

    updated_reminders = [r for r in reminders if r["id"] != reminder_id]

    if len(updated_reminders) == len(reminders):
        raise HTTPException(status_code=404, detail="Task not found")

    save_reminders(updated_reminders)

    return {"status": f"Task {reminder_id} deleted"}


# PUT /reminders/{reminder_id} — Edit reminder
@app.put("/reminders/{reminder_id}")
def update_reminder(reminder_id: int, data: dict):
    reminders = load_reminders()

    for reminder in reminders:
        if reminder["id"] == reminder_id:
            # Update fields if present
            if "task" in data:
                reminder["task"] = data["task"]
            if "time" in data:
                reminder["time"] = data["time"]
            save_reminders(reminders)
            return {"status": f"Reminder {reminder_id} updated"}

    raise HTTPException(status_code=404, detail="Reminder not found")

# Background scheduler
def check_reminders():
    reminders = load_reminders()
    now = datetime.now()
    notify_time = now + timedelta(minutes=1)

    for r in reminders:
        try:
            reminder_time = datetime.strptime(r["time"], "%I:%M%p")  # e.g., 6:10pm
            reminder_time = reminder_time.replace(year=now.year, month=now.month, day=now.day)
            
            if now < reminder_time <= notify_time:
                notification.notify(
                    title="⏰ Reminder in 30 mins",
                    message=f"{r['task']} at {r['time']}",
                    timeout=10
                )
        except Exception as e:
            print(f"Failed to parse reminder time: {r['time']}, Error: {e}")

# Start the background scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(check_reminders, "interval", seconds=60)
scheduler.start()

