import os
import chromadb

from pdf_loader import load_pdf
from chunker import chunk_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pdf_folder = os.path.join(BASE_DIR, "data", "pdfs")
db_path = os.path.join(BASE_DIR, "db")

os.makedirs(db_path, exist_ok=True)

client = chromadb.PersistentClient(path=db_path)

try:
    client.delete_collection("pdf_collection")
except:
    pass

collection = client.create_collection("pdf_collection")

if not os.path.exists(pdf_folder):
    raise RuntimeError(f"PDF folder not found: {pdf_folder}")

print("PDF folder:", pdf_folder)

for pdf_file in os.listdir(pdf_folder):

    if not pdf_file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(pdf_folder, pdf_file)

    print(f"Processing: {pdf_file}")

    text = load_pdf(pdf_path)

    chunks = chunk_text(text, chunk_size=500)

    for i, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk],
            ids=[f"{pdf_file}_{i}"],
            metadatas=[{
                "source": pdf_file,
                "chunk_id": i
            }]
        )

print("Database Created Successfully!")