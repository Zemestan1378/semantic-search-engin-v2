import chromadb

client = chromadb.PersistentClient(
    path="db"
)

collection = client.get_collection(
    name="knowledge"
)

while True:

    query = input(
        "\nSearch (q=quit): "
    )

    if query.lower() == "q":
        break

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    print("\nResults:\n")

    for doc in results["documents"][0]:
        print(doc)
        print()