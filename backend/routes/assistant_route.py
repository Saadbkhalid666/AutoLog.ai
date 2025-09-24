from flask import Blueprint, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
import torch #type: ignore

chat_bp = Blueprint("chat", __name__)

# Path to your locally trained Hugging Face model
model_path = Path(__file__).parent.parent / "autolog-ai-chatbot"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

# Device: CPU or GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@chat_bp.route("/c", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Encode user input only
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)

    # Generate reply
    chat_history_ids = model.generate(
        input_ids,
        max_length=200,           # max tokens
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=2,
        top_k=20,
        top_p=0.9,
        temperature=0.6
    )

    # Remove user input from generated output
    reply_ids = chat_history_ids[0][input_ids.shape[-1]:]
    reply = tokenizer.decode(reply_ids, skip_special_tokens=True).strip()
# Add Velix identity prefix if missing
    if "velix" not in reply.lower():   # lowercase for safety
        reply = "Velix reporting: " + reply


    return jsonify({"reply": reply})
