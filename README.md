# 🤖 Personal Assistant Chatbot

The **Personal Assistant Chatbot** is a Python-based modular assistant powered by FastAPI. It handles everyday tasks such as setting reminders, checking the weather, converting currencies, retrieving dictionary definitions, and summarizing Wikipedia topics. It uses an MCP (Model Context Protocol) architecture, with each feature handled by a separate microservice-like server.

---

## 📚 Features

This chatbot understands natural language input using intent parsing and responds with relevant information using specialized MCP servers. It supports:

- 📝 Creating, viewing, editing, and deleting reminders
- 🌦 Fetching real-time weather updates
- 💱 Performing currency conversion
- 📖 Looking up word definitions from a dictionary
- 🧠 Summarizing Wikipedia topics
- 🗂 Maintaining persistent conversation history across sessions

All user interactions are stored in a JSON file and can be viewed on request with `show my history`.

---

## ⚙️ How It Works

- **Intent Parsing**: User input is parsed to determine the intent (e.g., reminder creation, currency conversion).
- **Client Request Routing**: The parsed data is passed to a corresponding MCP client (reminder, weather, etc.).
- **MCP Server Handling**: Each client sends a request to its dedicated server that handles logic, fetches external data if needed, and returns a response.

---

## 🛠 Libraries Used

- `fastapi`: Backend API and server interfaces
- `requests`: For calling external APIs (e.g., OpenWeatherMap, ExchangeRate, Dictionary API)
- `python-dotenv`: Securely load API keys from environment
- `json`: Storing persistent conversation history

---

## 🌐 MCP Servers and Their Functions

| Server           | Purpose                                                  |
|------------------|----------------------------------------------------------|
| Reminder Server  | Create, list, delete, or edit reminders                 |
| Weather Server   | Fetch current weather for a location                    |
| Finance Server   | Convert currency using real-time exchange rates         |
| Wikipedia Server | Provide summaries for topics based on user queries      |
| Dictionary Server| Return definitions for English words                    |

Each server exposes a single endpoint (e.g., `/weather`, `/reminder`, etc.) that the backend calls based on user input.

---

## 💬 Example Prompts

Here are some example phrases you can use with the chatbot:

- **Reminders**:  
  - `Remind me to submit my assignment at 5pm`  
  - `Edit reminder 2 to call Alice at 6pm`  
  - `Delete task 1`  
  - `Show my reminders`

- **Weather**:  
  - `What’s the weather in Bangalore?`  
  - `Check the temperature in Tokyo`

- **Currency Conversion**:  
  - `Convert 100 USD to INR`  
  - `How much is 50 EUR in JPY?`

- **Dictionary**:  
  - `Define ephemeral`  
  - `What does serendipity mean?`

- **Wikipedia**:  
  - `Who is Alan Turing?`  
  - `Tell me about Machine Learning`

- **Conversation History**:  
  - `Show my history`

---

## 🚀 Future Enhancements

- **LLM Integration**: Replace rule-based intent parsing with a language model like GPT for more flexible conversation handling.
- **Voice Chat**: Enable voice input/output using speech recognition and TTS engines like `pyttsx3` or Google Speech API.
- **UI/UX**: Add a front-end using React or Flutter to make the assistant more user-friendly.
- **Multi-user Support**: Enable user profiles and authentication to manage different user histories and reminders.

---

## 📌 Summary

This chatbot is a great example of building a modular, extensible system using clean API boundaries. The MCP architecture ensures scalability — allowing easy addition of new features in isolated services without modifying the core logic.

