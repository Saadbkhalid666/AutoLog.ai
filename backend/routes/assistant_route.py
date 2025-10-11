from flask import Blueprint, request, jsonify #type:ignore
from transformers import AutoTokenizer, AutoModelForCausalLM #type:ignore
from pathlib import Path 
import torch #type:ignore

chat_bp = Blueprint("chat", __name__)

model_path = Path(__file__).parent.parent / "autolog-ai-chatbot"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@chat_bp.route("/c", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)

    chat_history_ids = model.generate(
        input_ids,
        max_length=200,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=2,
        top_k=20,
        top_p=0.9,
        temperature=0.6
    )

    reply_ids = chat_history_ids[0][input_ids.shape[-1]:]
    reply = tokenizer.decode(reply_ids, skip_special_tokens=True).strip()
 

    return jsonify({"reply": reply})
