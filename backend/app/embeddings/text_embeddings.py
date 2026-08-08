from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str) -> list[float]:
    embedding = get_embedding_model().encode(text)
    return embedding.tolist()