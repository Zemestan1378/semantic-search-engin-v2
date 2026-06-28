import chromadb


client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_collection(
    name="pdf_collection"
)


question = input(
    "Question: "
)

results = collection.query(
    query_texts=[question],
    n_results=3
)


print("\nResults:\n")

for doc in results["documents"][0]:

    print(doc)
    print()
    print("-" * 50)