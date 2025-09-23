from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset
from pathlib import Path

model_name = "microsoft/DialoGPT-small"

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token  # <-- important fix
model = AutoModelForCausalLM.from_pretrained(model_name)

# Dataset path
dataset_path = Path(__file__).parent.parent / "autos_train.json"
dataset = load_dataset("json", data_files={"train": str(dataset_path)})

# Tokenization function
def tokenize_function(example):
    text = example["user"] + tokenizer.eos_token + example["bot"] + tokenizer.eos_token
    tokenized = tokenizer(text, truncation=True, padding="max_length", max_length=128)
    tokenized["labels"] = tokenized["input_ids"]  # <-- add labels
    return tokenized


tokenized_datasets = dataset.map(tokenize_function, batched=False)

# Training arguments
output_dir = Path(__file__).parent.parent / "autolog-ai-chatbot"
training_args = TrainingArguments(
    output_dir=str(output_dir),
    num_train_epochs=3,
    per_device_train_batch_size=2,
    learning_rate=5e-5,
    weight_decay=0.01,
    save_total_limit=2,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"]
)

# Train & save
trainer.train()
trainer.save_model(str(output_dir))
tokenizer.save_pretrained(str(output_dir))

print(f"Training complete! Model saved to {output_dir}")
