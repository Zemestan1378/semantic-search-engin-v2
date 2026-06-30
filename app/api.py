from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import subprocess
import sys
import chromadb
subprocess.run(
    [sys.executable, "app/download_pdfs.py"],
    check=True
)

subprocess.run(
    [sys.executable, "app/build_pdf_chroma.py"],
    check=True
)
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

app = FastAPI()

# =====================
# Templates
# =====================

templates = Jinja2Templates(directory="app/templates")

# =====================
# ChromaDB
# =====================
# =====================
# ChromaDB
# =====================

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("pdf_collection")
# =====================
# Model
# =====================

MODEL_NAME = "google/flan-t5-small"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

# =====================
# Memory
# =====================

chat_history = []

# =====================
# Home
# =====================

@app.get("/")
def home():
    return {
        "message": "PDF RAG API Running"
    }

# =====================
# Ask API
# =====================

@app.get("/ask")
def ask(question: str):

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = "\n".join(
        results["documents"][0]
    )
    sources = list(
    set(
        [
            m["source"]
            for m in results["metadatas"][0]
        ]
    )
 )
    prompt = f"""
Use the context below to answer.

Context:
{context}

Question:
{question}

If the answer is not in the context, say:
I don't know.

Answer:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    return {
    "question": question,
    "answer": answer,
    "sources": sources
   }
     
# =====================
# Chat Page
# =====================

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
            "question": "",
            "answer": ""
        }
    )

# =====================
# Chat Submit
# =====================

@app.post("/chat", response_class=HTMLResponse)
async def chat(
    request: Request,
    question: str = Form(...)
):

    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    context = "\n".join(
        results["documents"][0]
    )
    sources = list(
    set(
        [
            m["source"]
            for m in results["metadatas"][0]
        ]
    )
   )   
    history_text = "\n".join(
        chat_history[-6:]
    )

    prompt = f"""
Conversation:
{history_text}

Context:
{context}

Question:
{question}

Answer using only the context.

If the answer is not in the context say:
I don't know.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=150
    )

    answer = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    chat_history.append(
        f"User: {question}"
    )

    chat_history.append(
        f"Assistant: {answer}"
    )

    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={
       "question": question,
       "answer": answer,
        "sources": sources
      }
    )