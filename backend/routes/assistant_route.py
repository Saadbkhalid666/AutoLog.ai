from flask import Blueprint, request, jsonify  # type:ignore
import requests  # type:ignore
import os  # type:ignore

chat_bp = Blueprint("chat", __name__)

# ✅ OpenRouter Settings
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "sk-or-v1-REPLACE_WITH_YOURS"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-4o-mini"   

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
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",   
        "X-Title": "AutoLog AI"  
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

    except requests.exceptions.HTTPError as http_err:
        # Extract OpenRouter’s actual error message if available
        try:
            error_data = response.json()
            return jsonify({"error": error_data.get("error", {}).get("message", str(http_err))}), response.status_code
        except:
            return jsonify({"error": f"AI request failed: {str(http_err)}"}), 503

    except requests.exceptions.Timeout:
        return jsonify({"error": "AI timed out. Please try again."}), 504
    except Exception as e:
        return jsonify({"error": f"AI request failed: {str(e)}"}), 503
