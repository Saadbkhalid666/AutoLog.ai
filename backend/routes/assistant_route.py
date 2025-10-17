from flask import Blueprint, request, jsonify #type:ignore
import requests #type:ignore
import os #type:ignore

chat_bp = Blueprint("chat", __name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_API_KEY}"

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

    payload = {
        "contents": [
            {"parts": [{"text": SYSTEM_PROMPT}]},
            {"parts": [{"text": user_message}]}
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=15)
        response.raise_for_status()  # Raises HTTPError for bad status codes
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Gemini API request failed: {str(e)}"}), 503

    try:
        candidates = response.json().get("candidates", [])
        if not candidates:
            return jsonify({"error": "No candidates returned by Gemini"}), 500
        reply = candidates[0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    except (KeyError, IndexError, ValueError) as e:
        return jsonify({"error": f"Unexpected Gemini response format: {str(e)}"}), 500
