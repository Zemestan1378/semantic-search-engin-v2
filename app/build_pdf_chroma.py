import os
import chromadb

from pdf_loader import load_pdf
from chunker import chunk_text

# PDF folder
pdf_folder = "data/pdfs"

# ChromaDB
client = chromadb.PersistentClient(
    path="db"
)

try:
    client.delete_collection(
        "pdf_collection"
    )
except:
    pass

collection = client.create_collection(
    name="pdf_collection"
)

# Process PDFs
for pdf_file in os.listdir(pdf_folder):

    if not pdf_file.endswith(".pdf"):
        continue

    pdf_path = os.path.join(
        pdf_folder,
        pdf_file
    )

    print(
        f"Processing: {pdf_file}"
    )

    text = load_pdf(
        pdf_path
    )

    chunks = chunk_text(
        text,
        chunk_size=500
    )

    for i, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk],
            ids=[
                f"{pdf_file}_{i}"
            ],
            metadatas=[
                {
                    "source": pdf_file,
                    "chunk_id": i
                }
            ]
        )

print(
    "Database Created Successfully!"
)