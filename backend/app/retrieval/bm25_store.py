from rank_bm25 import BM25Okapi

from app.retrieval.chroma_store import get_collection


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def query_keywords(question: str, n_results: int = 5) -> list[dict]:
    collection = get_collection()
    results = collection.get(include=["documents", "metadatas", "ids"])

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])
    ids = results.get("ids", [])

    if not documents:
        return []

    tokenized_corpus = [_tokenize(document) for document in documents]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(_tokenize(question))

    ranked_indices = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)[:n_results]

    return [
        {
            "id": ids[index],
            "text": documents[index],
            "metadata": metadatas[index],
            "score": float(scores[index]),
        }
        for index in ranked_indices
    ]