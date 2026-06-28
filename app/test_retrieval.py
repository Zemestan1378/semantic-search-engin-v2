import chromadb

client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_collection(
    "pdf_collection"
)

query = input("Question: ")

results = collection.query(
    query_texts=[query],
    n_results=3
)

for doc in results["documents"][0]:

    print()
    print(doc)
    print("-" * 50)