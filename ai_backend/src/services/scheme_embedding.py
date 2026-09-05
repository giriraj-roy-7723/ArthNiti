# src/services/scheme_embedding.py

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"

_model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    embedding = _model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()
