import chromadb
from document import load_documents

documents = load_documents(
    "data/knowledge.txt"
)

client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_or_create_collection(
    name="knowledge"
)

collection.add(
    documents=documents,
    ids=[str(i) for i in range(len(documents))]
    metadatas=[{
        "chunk_id": i
    }]
)
)

print("Documents added!")