from document import load_documents

from embeddings import (
    create_embeddings,
    save_embeddings
)

documents = load_documents(
    "data/knowledge.txt"
)

embeddings = create_embeddings(
    documents
)

save_embeddings(
    embeddings,
    "data/embeddings.pkl"
)

print(
    "Embeddings saved!"
)