from fastapi import FastAPI, Request
from typing import Dict
import requests

app = FastAPI()

ER_API_BASE_URL = "https://open.er-api.com/v6/latest"

@app.post("/mcp")
async def convert_currency(request: Request) -> Dict[str, str]:
    try:
        body = await request.json()
        amount = body.get("amount")
        from_currency = body.get("from_currency")
        to_currency = body.get("to_currency")

        # Validate inputs
        if not all([amount, from_currency, to_currency]):
            return {"error": "Missing amount or currency codes"}

        # Get exchange rates from ER API
        api_url = f"{ER_API_BASE_URL}/{from_currency.upper()}"
        res = requests.get(api_url, timeout=5)

        if res.status_code != 200:
            return {"error": "Failed to fetch exchange rates"}

        data = res.json()
        rates = data.get("rates", {})

        if to_currency.upper() not in rates:
            return {"error": f"Currency '{to_currency}' not supported"}

        rate = rates[to_currency.upper()]
        converted = float(amount) * rate

        return {
            "converted": f"{amount} {from_currency.upper()} = {converted:.2f} {to_currency.upper()}",
            "rate": f"1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"
        }

    except Exception as e:
        return {"error": str(e)}
