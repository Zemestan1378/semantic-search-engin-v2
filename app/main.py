from search import SemanticSearch

# داده‌ها را می‌خوانیم
with open(r"C:\Users\MEHR\Downloads\AI_project\semantic-search-engin\data\document.txt", "r", encoding="utf-8") as f:
    documents = f.read().splitlines()

search_engine = SemanticSearch(documents)

print("Semantic Search Ready 🚀")

while True:
    query = input("\nEnter query: ")

    results = search_engine.search(query)

    print("\nTop results:")
    for doc, score in results:
        print(f"{score:.4f} -> {doc}")