import requests

BASE_URL = "http://localhost:8000"

def create_reminder(task: str, time: str) -> str:
    payload = {"task": task, "time": time}
    try:
        res = requests.post(f"{BASE_URL}/reminder", json=payload)
        return res.json().get("status", "error creating reminder")
    except Exception as e:
        return f"Error: {str(e)}"

def view_reminders() -> str:
    try:
        res = requests.get(f"{BASE_URL}/reminders")
        if res.status_code == 200:
            reminders = res.json()
            return "\n".join([f"{r['id']}: {r['task']} at {r['time']}" for r in reminders])
        else:
            return "Failed to fetch reminders"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_reminder(reminder_id: int) -> str:
    try:
        res = requests.delete(f"{BASE_URL}/reminder/{reminder_id}")
        if res.status_code == 200:
            return res.json().get("status", "Task deleted")
        elif res.status_code == 404:
            return "Task not found"
        else:
            return "Failed to delete task"
    except Exception as e:
        return f"Error: {str(e)}"


def update_reminder(reminder_id: int, task: str, time: str) -> str:
    try:
        res = requests.put(f"{BASE_URL}/reminder/{reminder_id}", json={"task": task, "time": time})
        if res.status_code == 200:
            return res.json().get("status", "Reminder updated")
        elif res.status_code == 404:
            return "Reminder not found"
        else:
            return "Failed to update reminder"
    except Exception as e:
        return f"Error: {str(e)}"