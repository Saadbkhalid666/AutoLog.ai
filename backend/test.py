import json
import random

# Load existing dataset
with open("autos_train.json", "r") as f:
    data = json.load(f)

# Function to expand answers
def expand_answer(short_answer):
    # Split by "." or "," to create step-like sentences
    base_steps = short_answer.replace("Velix reporting.", "").split(".")
    steps = []
    for step in base_steps:
        step = step.strip()
        if step:
            # Add numbering for steps
            steps.append(step)
    # Randomly add 1-2 more descriptive steps for realism
    extras = [
        "Ensure all tools are ready before starting",
        "Double-check measurements",
        "Follow safety precautions",
        "Refer to the car manual for specifics",
        "Repeat the process if unsure"
    ]
    random.shuffle(extras)
    steps += extras[:2]
    # Join as numbered steps
    expanded = ""
    for i, s in enumerate(steps, 1):
        expanded += f"{i}. {s}. "
    expanded += "Velix reporting."
    return expanded

# Expand dataset
expanded_data = []
for entry in data:
    user_q = entry["user"]
    bot_a = entry["bot"]
    expanded_a = expand_answer(bot_a)
    expanded_data.append({
        "user": user_q,
        "bot": expanded_a
    })

# Save expanded dataset
with open("autos_train_expanded.json", "w") as f:
    json.dump(expanded_data, f, indent=2)

print(f"✅ Expanded dataset saved with {len(expanded_data)} entries.")
