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

print("🤖 Personal Assistant Chatbot (type 'exit' to quit)")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break
   
    # Dictionary intent
    word = parse_dictionary(user_input)
    if word:
        response = get_definition(word)
        print(f"Bot: {response}")
        continue

    # Wikipedia intent
    query = parse_wikipedia_query(user_input)
    if query:
        response = get_wiki_summary(query)
        print(f"Bot: {response}")
        continue

    # Currency Conversion intent
    conversion = parse_currency_conversion(user_input)
    if conversion:
        amount, from_currency, to_currency = conversion
        response = get_conversion_result(amount, from_currency, to_currency)
        print(f"Bot: {response}")
        continue

    # Weather intent
    location = parse_weather(user_input)
    if location:
        response = get_weather(location)
        print(f"Bot: {response}")
        continue

    # Reminder creation
    result = parse_reminder(user_input)
    if result:
        task, time = result
        response = create_reminder(task, time)
        print(f"Bot: {response}")
        continue

    # View reminders
    elif "show my reminders" in user_input.lower() or "show my tasks" in user_input.lower():
        response = view_reminders()
        print(f"Bot:\n{response}")
        continue

    # Delete reminder
    elif "delete reminder" in user_input.lower() or "remove reminder" in user_input.lower() or "delete task" in user_input.lower() or "remove task" in user_input.lower():
        words = user_input.strip().split()
        try:
            reminder_id = int(words[-1])
            response = delete_reminder(reminder_id)
            print(f"Bot: {response}")
        except ValueError:
            print("Bot: Please specify a valid reminder ID to delete.")
        continue

    # Edit reminder
    elif "edit task" in user_input.lower() or "update task" in user_input.lower() or "change task" in user_input.lower():
        parsed = parse_edit_reminder(user_input)
        if parsed:
            reminder_id, task, time = parsed
            response = update_reminder(reminder_id, task, time)
            print(f"Bot: {response}")
        else:
            print("Bot: Please use a format like 'change reminder 2 to call dad at 7pm'")
        continue

    else:
        print("Bot: I can help you with reminders, weather, and currency conversion.")
        print("     Try: convert 100 usd to inr or remind me to drink water at 3pm")
