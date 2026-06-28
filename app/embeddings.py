import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(documents):

    return model.encode(documents)


def save_embeddings(
    embeddings,
    filename
):

    with open(
        filename,
        "wb"
    ) as f:

        pickle.dump(
            embeddings,
            f
        )


def load_embeddings(
    filename
):

    with open(
        filename,
        "rb"
    ) as f:

        return pickle.load(f)