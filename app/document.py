def load_documents(path):
    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    docs = [
        doc.strip()
        for doc in text.split("\n\n")
        if doc.strip()
    ]

    return docs