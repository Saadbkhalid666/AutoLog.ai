from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv
import requests
import os

# Load environment variables
load_dotenv()

# Flask app
app = Flask(__name__)

# Blueprint for Nex chat
chat_bp = Blueprint("chat", __name__)

# Gemini API Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"

# Nex system prompt (formal AI assistant)
SYSTEM_PROMPT = (
    "Your name is Nex. You are an intelligent automotive maintenance assistant inside the AutoLog.AI platform. "
    "You respond formally and professionally. Your primary goal is to assist users with car maintenance, "
    "fuel efficiency, service reminders, and automotive best practices. Keep responses clear, precise, and informative."
)

@chat_bp.route("/c", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Minimal payload for Gemini
    payload = {
        "contents": [
            {"parts": [{"text": SYSTEM_PROMPT}]},
            {"parts": [{"text": user_message}]}
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=20)
        if response.status_code == 200:
            result_json = response.json()
            # Extract reply safely
            try:
                reply = result_json["candidates"][0]["content"]["parts"][0]["text"]
                return jsonify({"reply": reply})
            except Exception as e:
                return jsonify({"error": "Unexpected Gemini response format", "details": str(e)}), 500
        else:
            return jsonify({"error": f"Failed to get response from Nex (status {response.status_code})", "details": response.text}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request to Gemini API failed", "details": str(e)}), 500

# Register blueprint
app.register_blueprint(chat_bp)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)
