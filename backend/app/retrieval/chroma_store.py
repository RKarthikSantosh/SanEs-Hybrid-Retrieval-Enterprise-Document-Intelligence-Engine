from functools import lru_cache

from chromadb import PersistentClient

from app.embeddings.text_embeddings import embed_text


CHROMA_PATH = "data/chroma"
COLLECTION_NAME = "document_chunks"


@lru_cache(maxsize=1)
def get_collection():
    client = PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def store_chunks(chunks: list[dict]) -> None:
    if not chunks:
        return

    collection = get_collection()
    collection.upsert(
        ids=[f"{chunk['filename']}-{chunk['chunk_id']}" for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        metadatas=[
            {
                "chunk_id": chunk["chunk_id"],
                "page": chunk["page"],
                "filename": chunk["filename"],
            }
            for chunk in chunks
        ],
    )


def query_chunks(query: str, n_results: int = 3) -> dict:
    collection = get_collection()
    return collection.query(
        query_embeddings=[embed_text(query)],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )