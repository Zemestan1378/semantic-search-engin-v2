import chromadb

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

MODEL_NAME = "google/flan-t5-base"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Model Ready!")

client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_collection(
    "pdf_collection"
)

while True:

    question = input(
        "\nQuestion (q=quit): "
    )

    if question.lower() == "q":
        break

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer in a complete sentence.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=120
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    print()
    print("Retrieved Context")
    print("-" * 50)
    print(context)

    print()
    print("Answer")
    print("-" * 50)
    print(answer)