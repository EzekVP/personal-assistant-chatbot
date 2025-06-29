from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, Any, Optional
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Never hardcode your API key

def chat_with_llm(message: str) -> Optional[Dict[str, Any]]:
    """
    Calls the LLM with the user message and returns the parsed intent and parameters.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",  # or "gpt-3.5-turbo-1106"
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts intent and details from messages. Respond only with a JSON object."
                },
                {
                    "role": "user",
                    "content": message
                }
            ],
            functions=[
                {
                    "name": "create_reminder",
                    "description": "Create a reminder for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "The task to remind the user about"
                            },
                            "time": {
                                "type": "string",
                                "description": "Time of the reminder, e.g., '7pm'"
                            }
                        },
                        "required": ["task", "time"]
                    }
                }
            ],
            function_call="auto"
        )

        if response.choices and response.choices[0].message.function_call:
            fn = response.choices[0].message.function_call
            return {
                "function": fn.name,
                "arguments": fn.arguments  # This is a JSON string — we'll parse it in the next step
            }

        return None

    except Exception as e:
        print(f"LLM Error: {e}")
        return None
