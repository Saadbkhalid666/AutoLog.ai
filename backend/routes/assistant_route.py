from flask import Blueprint, request, jsonify #type:ignore
import requests #type:ignore
import os #type:ignore

chat_bp = Blueprint("chat", __name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY_HERE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
params = { "key": GEMINI_API_KEY }

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

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    headers = { "Content-Type": "application/json" }
    params = { "key": GEMINI_API_KEY }

    payload = {
            "system_instruction": {
                "parts": [{"text": SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "parts": [{"text": user_message}]
                }
            ]
        }

    try:
        response = requests.post(url, headers=headers, params=params, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        reply = data["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"reply": reply})
    
    except requests.exceptions.Timeout:
        return jsonify({"error": "Gemini timed out. Please try again."}), 504
    except Exception as e:
        return jsonify({"error": f"Gemini API request failed: {str(e)}"}), 503
