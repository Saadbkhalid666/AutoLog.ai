from flask import Blueprint, jsonify, request
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
import torch

chat_bp = Blueprint("chat", __name__)

# Model path
model_path = Path(__file__).parent.parent / "autolog-ai-chatbot"

# Load trained model & tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Encode input
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")

    # Generate reply
    chat_history_ids = model.generate(
        input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id
    )
    
    reply = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
    return jsonify({"reply": reply})
