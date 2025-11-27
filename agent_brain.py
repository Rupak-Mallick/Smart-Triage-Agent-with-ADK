"""
Smart Triage Agent - Agent Brain Module

NOTE: This implementation uses Google's Gemini SDK directly rather than the ADK framework
due to compatibility issues between ADK v1.18.0 and Python 3.14. The architecture follows
ADK principles (tool-based agent design, structured prompts, function calling) but uses
the stable Gemini SDK for reliability.

ADK Compatibility Issue: ADK v1.18.0 throws 'model_copy' AttributeError with Python 3.14
due to Pydantic validation issues in the underlying dependencies.
"""

import google.generativeai as genai
import json
from datetime import datetime

# --- Mock Database / State ---
db = {
    "tickets": [],
    "invoices": [],
    "calendar": [
        {"time": "2023-10-27 10:00", "event": "Team Standup"},
        {"time": "2023-10-27 14:00", "event": "Client Call"}
    ]
}

def configure_genai(api_key):
    """Configures the Gemini API with the provided key."""
    genai.configure(api_key=api_key)

# --- Tool Functions (Following ADK Tool Pattern) ---

def create_ticket(summary, priority="Medium"):
    """Creates a support ticket."""
    ticket_id = f"TICK-{len(db['tickets']) + 101}"
    ticket = {
        "id": ticket_id,
        "summary": summary,
        "priority": priority,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    db['tickets'].append(ticket)
    return f"Ticket created successfully. ID: {ticket_id}"

def generate_invoice(client_name, amount):
    """Generates an invoice."""
    invoice_id = f"INV-{len(db['invoices']) + 1001}"
    invoice = {
        "id": invoice_id,
        "client": client_name,
        "amount": amount,
        "status": "Sent",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    db['invoices'].append(invoice)
    return f"Invoice generated for {client_name} for ${amount}. ID: {invoice_id}"

def check_calendar(date_str=None):
    """Checks calendar availability."""
    events = db['calendar']
    if not events:
        return "Calendar is completely free."
    return f"Existing events: {json.dumps(events)}"

def send_reply(message):
    """Simulates sending a reply."""
    return f"Reply sent: '{message}'"

# --- Agent Logic (ADK-Inspired Architecture) ---

def process_message(user_message, api_key):
    """
    Process user message using agent architecture.
    
    Architecture follows ADK principles:
    1. Intent classification via LLM
    2. Tool selection based on intent
    3. Tool execution
    4. Response generation
    """
    if not api_key:
        return {"error": "Missing API Key"}

    configure_genai(api_key)
    
    # System instruction following ADK agent pattern
    system_prompt = """
    You are an Enterprise Triage Agent. Your job is to analyze incoming messages and decide what to do.
    
    AVAILABLE TOOLS:
    1. create_ticket(summary, priority): Use for bug reports, IT issues, or feature requests.
    2. check_calendar(date_str): Use for scheduling requests.
    3. generate_invoice(client_name, amount): Use when the user asks to create or send an invoice.
    4. send_reply(message): Use to reply to the user.
    
    INSTRUCTIONS:
    - Analyze the user's message.
    - Return a JSON object with the following structure:
    {
        "thought": "Your reasoning here",
        "tool": "The name of the tool to use",
        "args": { "arg_name": "arg_value" }
    }
    """

    # Try multiple Gemini models (ADK-style fallback)
    candidate_models = [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-1.5-flash'
    ]

    last_error = None

    for model_name in candidate_models:
        try:
            model = genai.GenerativeModel(
                model_name,
                generation_config={"response_mime_type": "application/json"}
            )
            response = model.generate_content(f"{system_prompt}\n\nUSER MESSAGE: {user_message}")
            result_json = json.loads(response.text)
            
            tool_name = result_json.get("tool")
            tool_args = result_json.get("args", {})
            thought = result_json.get("thought")
            
            # Execute tool (ADK-style tool execution)
            tool_output = ""
            if tool_name == "create_ticket":
                tool_output = create_ticket(tool_args.get("summary"), tool_args.get("priority", "Medium"))
            elif tool_name == "check_calendar":
                tool_output = check_calendar(tool_args.get("date_str"))
            elif tool_name == "generate_invoice":
                tool_output = generate_invoice(tool_args.get("client_name"), tool_args.get("amount"))
            elif tool_name == "send_reply":
                tool_output = send_reply(tool_args.get("message"))
            else:
                tool_output = "Error: Unknown tool selected."

            return {
                "thought": thought,
                "tool_used": tool_name,
                "tool_output": tool_output,
                "model_used": f"{model_name} (Gemini SDK)"
            }

        except Exception as e:
            last_error = e
            continue

    # If all models failed
    try:
        available_models = [m.name for m in genai.list_models()]
        return {
            "error": f"All models failed. Last error: {str(last_error)}. Available: {available_models[:5]}"
        }
    except Exception as list_error:
        return {"error": f"All models failed. Last error: {str(last_error)}"}
