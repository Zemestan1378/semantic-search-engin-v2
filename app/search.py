from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

from document import load_documents

documents = load_documents(
    "data/knowledge.txt"
)
from embeddings import (
    load_embeddings
)

doc_embeddings = load_embeddings(
    "data/embeddings.pkl"
)

while True:

    query = input("\nSearch (q=quit): ")

    if query.lower() == "q":
        print("Goodbye!")
        break

    query_embedding = model.encode([query])

    scores = cosine_similarity(
        query_embedding,
        doc_embeddings
    )

    top_k = 3

    top_indices = np.argsort(
        scores[0]
    )[::-1][:top_k]

    print("\nTop Results:\n")

    for rank, idx in enumerate(
        top_indices,
        start=1
    ):

        print(
            f"{rank}. {documents[idx]}"
        )

        print(
            f"Score: {scores[0][idx]:.4f}"
        )

        print()



