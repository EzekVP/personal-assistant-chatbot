import json
import os
from intent_parser import (
    parse_reminder,
    parse_edit_reminder,
    parse_weather,
    parse_currency_conversion,
    parse_wikipedia_query,
    parse_dictionary
)
from reminder_client import create_reminder, view_reminders, delete_reminder, update_reminder
from weather_client import get_weather
from finance_client import get_conversion_result
from wiki_client import get_wiki_summary
from dictionary_client import get_definition 

HISTORY_FILE = "chatbot/conversation_history.json"

# Load conversation history if it exists
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        conversation_history = json.load(f)
else:
    conversation_history = []

print("🤖 Personal Assistant Chatbot (type 'exit' to quit)")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    # ✅ Show conversation history
    if user_input.lower() in ["show my history", "show chat log", "show conversation", "chat history"]:
        if conversation_history:
            print("\n📜 Conversation History:\n")
            for i, entry in enumerate(conversation_history, start=1):
                print(f"{i}. You: {entry['user']}")
                print(f"   Bot: {entry['bot']}\n")
        else:
            print("Bot: No conversation history found.")
        continue

    response = ""

    # Dictionary intent
    word = parse_dictionary(user_input)
    if word:
        response = get_definition(word)

    # Wikipedia intent
    elif (query := parse_wikipedia_query(user_input)):
        response = get_wiki_summary(query)

    # Currency Conversion intent
    elif (conversion := parse_currency_conversion(user_input)):
        amount, from_currency, to_currency = conversion
        response = get_conversion_result(amount, from_currency, to_currency)

    # Weather intent
    elif (location := parse_weather(user_input)):
        response = get_weather(location)

    # Reminder creation
    elif (result := parse_reminder(user_input)):
        task, time = result
        response = create_reminder(task, time)

    # View reminders
    elif "show my reminders" in user_input.lower() or "show my tasks" in user_input.lower():
        response = view_reminders()

    # Delete reminder
    elif any(keyword in user_input.lower() for keyword in ["delete reminder", "remove reminder", "delete task", "remove task"]):
        words = user_input.strip().split()
        try:
            reminder_id = int(words[-1])
            response = delete_reminder(reminder_id)
        except ValueError:
            response = "Please specify a valid reminder ID to delete."

    # Edit reminder
    elif "edit task" in user_input.lower() or "update task" in user_input.lower() or "change task" in user_input.lower():
        parsed = parse_edit_reminder(user_input)
        if parsed:
            reminder_id, task, time = parsed
            response = update_reminder(reminder_id, task, time)
        else:
            response = "Please use a format like 'change reminder 2 to call dad at 7pm'"

    else:
        response = (
            "I can help you with reminders, weather, currency conversion, definitions, and summaries.\n"
            "Try: convert 100 usd to inr or remind me to drink water at 3pm"
        )

    print(f"Bot: {response}")

    # ✅ Save conversation to persistent history
    conversation_history.append({"user": user_input, "bot": response})
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(conversation_history, f, indent=2)
