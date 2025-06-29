from intent_parser import parse_reminder, parse_edit_reminder
from reminder_client import create_reminder, view_reminders, delete_reminder, update_reminder

print("🤖 Personal Assistant Chatbot (type 'exit' to quit)")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    #  Parse and create a reminder
    result = parse_reminder(user_input)
    if result:
        task, time = result
        response = create_reminder(task, time)
        print(f"Bot: {response}")
        continue

    #  View reminders
    elif "show my reminders" in user_input.lower() or "show my tasks" in user_input.lower():
        response = view_reminders()
        print(f"Bot:\n{response}")
        continue

    #  Delete reminder
    elif "delete reminder" in user_input.lower() or "remove reminder" in user_input.lower() or "delete task" in user_input.lower() or "remove task" in user_input.lower():
        words = user_input.strip().split()
        try:
            reminder_id = int(words[-1])
            response = delete_reminder(reminder_id)
            print(f"Bot: {response}")
        except ValueError:
            print("Bot: Please specify a valid reminder ID to delete.")
        continue

    # Edit / Change reminder
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
        print("Bot: I can help you set, view, or delete reminders.")
        print("     Try: remind me to drink water at 3pm")
