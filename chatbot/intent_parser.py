import re
from typing import Optional, Tuple

def parse_reminder(text: str) -> Optional[Tuple[str, str]]:
    text = text.lower()

    patterns = [
        r"remind me to (.+) at (.+)",
        r"remind me at (.+) to (.+)",
        r"set a reminder to (.+) at (.+)",
        r"add reminder: (.+) at (.+)"
    ]

    for pattern in patterns:
        match = re.match(pattern, text)
        if match:
            # Handle flipped groups if time comes first
            if "at" in pattern and pattern.index("at") < pattern.index("to"):
                time, task = match.groups()
            else:
                task, time = match.groups()
            return task.strip(), time.strip()

    return None

def parse_edit_reminder(text: str) -> Optional[Tuple[int, str, str]]:
    """
    Extracts (id, task, time) from:
    'change reminder 2 to call mom at 7pm'
    """
    pattern = r"(?:change|update) task (\d+) to (.+) at (.+)"
    match = re.match(pattern, text.strip().lower())
    if match:
        reminder_id, task, time = match.groups()
        return int(reminder_id), task.strip(), time.strip()
    return None

def parse_weather(text: str) -> Optional[str]:
    """
    Extracts location from user text like 'weather in Mumbai'
    """
    pattern = r"(?:weather|temperature|forecast) in ([a-zA-Z\s]+)"
    match = re.search(pattern, text.lower())
    if match:
        return match.group(1).strip()
    return None
