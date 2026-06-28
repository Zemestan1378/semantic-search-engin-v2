from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading model...")
model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

question = "What is Artificial Intelligence?"

inputs = tokenizer(
    question,
    return_tensors="pt"
)

outputs = model.generate(
    **inputs,
    max_new_tokens=50
)

answer = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("\nAnswer:")
print(answer)