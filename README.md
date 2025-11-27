# Smart Triage Agent

An intelligent enterprise triage system that automatically processes incoming messages, classifies intents, and executes appropriate actions using Google's Gemini AI.

## Features

- **Automated Ticket Creation**: Automatically creates support tickets for bug reports and IT issues
- **Invoice Generation**: Generates invoices based on natural language requests
- **Calendar Management**: Checks availability and schedules meetings
- **Smart Intent Classification**: Uses Gemini AI to understand user intent
- **Real-time Dashboard**: Clean, responsive UI built with Flask and Tailwind CSS

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **AI Framework**: Google Gemini SDK (ADK-inspired architecture)
- **AI Model**: Google Gemini 2.5 Flash
- **Data Storage**: In-memory (JSON)

**Note on ADK**: This project follows Google ADK architectural principles (tool-based agents, structured prompts, function calling) but uses the Gemini SDK directly due to compatibility issues between ADK v1.18.0 and Python 3.14.

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd "5-day AI Agents Intensive course!"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser to `http://127.0.0.1:5000`

3. Enter your Gemini API key in the dashboard

4. Type a message or select from examples:
   - "I forgot my password for the HR portal"
   - "Urgent! The payment gateway is throwing 500 errors"
   - "Please generate an invoice for Acme Corp for $1500"

## Project Structure

```
.
├── app.py                 # Flask application entry point
├── agent_brain.py         # AI agent logic and tool definitions
├── templates/
│   └── index.html        # Dashboard UI
├── requirements.txt       # Python dependencies
└── README.md
```

## How It Works

1. **User Input**: User submits a message through the web interface
2. **Intent Analysis**: Gemini AI analyzes the message and determines the appropriate action
3. **Tool Execution**: The agent executes the selected tool (create ticket, generate invoice, etc.)
4. **Response**: Results are displayed in real-time on the dashboard

## Available Tools

- `create_ticket(summary, priority)`: Creates support tickets
- `generate_invoice(client_name, amount)`: Generates invoices
- `check_calendar(date_str)`: Checks calendar availability
- `send_reply(message)`: Sends automated replies

## License

MIT

## Author

Built for the 5-day AI Agents Intensive Course
