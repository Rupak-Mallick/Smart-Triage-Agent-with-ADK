from flask import Flask, render_template, request, jsonify
import agent_brain
import os

app = Flask(__name__)

# --- Routes ---

@app.route('/')
def index():
    """Renders the main dashboard."""
    tickets = agent_brain.db['tickets']
    return render_template('index.html', tickets=reversed(tickets))

@app.route('/process', methods=['POST'])
def process():
    """API endpoint to process a message."""
    data = request.json
    message = data.get('message')
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({"error": "Missing API Key"}), 400

    # Call the Agent Brain
    result = agent_brain.process_message(message, api_key)
    
    if "error" in result:
        return jsonify(result), 400
    
    # Return result + updated ticket list
    return jsonify({
        "result": result,
        "tickets": list(reversed(agent_brain.db['tickets']))
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
