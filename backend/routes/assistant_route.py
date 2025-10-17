from flask import Blueprint, request, jsonify  # type:ignore
import requests  # type:ignore
import os  # type:ignore

chat_bp = Blueprint("chat", __name__)

# ✅ Use OpenRouter Instead of Gemini API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "sk-or-v1-YOUR_KEY_HERE"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ✅ Choose Model (works reliably)
OPENROUTER_MODEL = "openai/gpt-4o-mini"  # or "google/gemini-pro-1.5" / "google/gemini-2.0-flash-exp:free"

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

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except requests.exceptions.Timeout:
        return jsonify({"error": "AI request timed out. Please try again."}), 504
    except Exception as e:
        return jsonify({"error": f"AI request failed: {str(e)}"}), 503
