from flask import Blueprint, request, jsonify
import requests
import os

chat_bp = Blueprint("chat", __name__)

# Gemini API Config
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# Nex Identity (System Prompt)
SYSTEM_PROMPT = (
    "Your name is Nex. You are an intelligent automotive maintenance assistant inside the AutoLog.AI platform. "
    "You respond formally and professionally. Your primary goal is to assist users with car maintenance, "
    "fuel efficiency, service reminders, and automotive best practices. Keep responses clear, precise, and informative."
)

@chat_bp.route("/c", methods=["POST"])  # Keeping same route, change if needed
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Gemini API payload
    payload = {
        "contents": [
            {"parts": [{"text": SYSTEM_PROMPT}]},
            {"parts": [{"text": user_message}]}
        ]
    }

    response = requests.post(GEMINI_URL, json=payload)

    if response.status_code == 200:
        try:
            reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"reply": reply})
        except Exception:
            return jsonify({"error": "Unexpected Gemini response format"}), 500

    return jsonify({"error": "Failed to get response from Nex (Gemini API error)"}), 500
