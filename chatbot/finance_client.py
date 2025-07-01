import requests
from typing import Optional

BASE_URL = "http://localhost:8000"

def get_conversion_result(amount: float, from_currency: str, to_currency: str) -> Optional[str]:
    try:
        payload = {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency
        }
        res = requests.post(f"{BASE_URL}/finance", json=payload, timeout=5)

        if res.status_code != 200:
            return f"Error: {res.status_code} - {res.text}"

        data = res.json()
        if "converted" in data and "rate" in data:
            return f"{data['converted']} ({data['rate']})"
        else:
            return "Conversion failed."

    except Exception as e:
        return f"Error: {str(e)}"
