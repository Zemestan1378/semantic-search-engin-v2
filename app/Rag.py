import chromadb

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)


# -------------------------
# Load LLM
# -------------------------

print("Loading model...")

MODEL_NAME = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Model Ready!")


# -------------------------
# Load ChromaDB
# -------------------------

client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_collection(
    name="knowledge"
)


# -------------------------
# RAG Loop
# -------------------------

while True:

    question = input(
        "\nQuestion (q=quit): "
    )

    if question.lower() == "q":
        print("Goodbye!")
        break


    # Retrieve best matching document
    results = collection.query(
        query_texts=[question],
        n_results=1
    )


    context = "\n".join(
        results["documents"][0]
    )


    # Better Prompt
    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Give a short and clear answer based on the context.
"""


    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True
    )


    outputs = model.generate(
        **inputs,
        max_new_tokens=100
    )


    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )


    print("\nRetrieved Context:")
    print("-" * 40)
    print(context)

    print("\nAnswer:")
    print("-" * 40)
    print(answer)