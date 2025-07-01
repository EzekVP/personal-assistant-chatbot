import re
from typing import Optional, Tuple

# -------------------- Reminder Parsing --------------------
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
            if "at" in pattern and pattern.index("at") < pattern.index("to"):
                time, task = match.groups()
            else:
                task, time = match.groups()
            return task.strip(), time.strip()
    return None

# -------------------- Reminder Editing --------------------
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

# -------------------- Weather Parsing --------------------
def parse_weather(text: str) -> Optional[str]:
    """
    Extracts location from strings like:
    - what's the weather in mumbai
    - weather for london
    """
    text = text.strip().lower()
    weather_patterns = [
        r"(?:what's|what is)? ?the weather in ([a-zA-Z\s]+)",
        r"weather for ([a-zA-Z\s]+)",
        r"how's the weather in ([a-zA-Z\s]+)"
    ]
    for pattern in weather_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return None

# -------------------- Currency Conversion Parsing --------------------
def parse_currency_conversion(text: str) -> Optional[Tuple[float, str, str]]:
    """
    Extracts conversion request like:
    'convert 100 usd to inr'
    Returns: (100.0, 'usd', 'inr')
    """
    pattern = r"convert ([0-9]+(?:\.[0-9]+)?) ([a-zA-Z]{3}) to ([a-zA-Z]{3})"
    match = re.search(pattern, text.lower())
    if match:
        amount, from_currency, to_currency = match.groups()
        return float(amount), from_currency.upper(), to_currency.upper()
    return None
