from flask import Blueprint, jsonify, request #type: ignore
from transformers import AutoTokenizer, AutoModelForCausalLM #type: ignore
from pathlib import Path
import torch #type: ignore

chat_bp = Blueprint("chat", __name__)


# Model path
model_path = Path(__file__).parent.parent / "autolog-ai-chatbot"

# Load trained model & tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

@chat_bp.route("/c", methods=["POST"])
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
        max_length=200,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
    )

    # Decode output and clean reply
    output_text = tokenizer.decode(chat_history_ids[0], skip_special_tokens=True)
    reply = output_text.replace(user_input, "").strip()

    return jsonify({"reply": reply})

