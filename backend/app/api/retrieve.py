from pydantic import BaseModel
from fastapi import APIRouter

from app.retrieval.bm25_store import query_keywords
from app.retrieval.chroma_store import query_chunks

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


def _rank_fusion(vectors: list[dict], keywords: list[dict], limit: int = 5) -> list[dict]:
    merged: dict[str, dict] = {}

    def add_candidate(candidate: dict, source: str, rank: int) -> None:
        candidate_id = candidate.get("id") or f"{candidate.get('metadata', {}).get('filename', '')}-{candidate.get('metadata', {}).get('chunk_id', '')}-{candidate.get('text', '')}"
        if candidate_id not in merged:
            merged[candidate_id] = {
                "id": candidate_id,
                "text": candidate.get("text"),
                "metadata": candidate.get("metadata"),
                "score": 0.0,
                "sources": [],
            }
        merged[candidate_id]["score"] += 1.0 / (60 + rank)
        merged[candidate_id]["sources"].append(source)

    for index, candidate in enumerate(vectors, start=1):
        add_candidate(candidate, "vector", index)

    for index, candidate in enumerate(keywords, start=1):
        add_candidate(candidate, "keyword", index)

    return sorted(merged.values(), key=lambda item: item["score"], reverse=True)[:limit]


@router.post("/query")
def query_documents(request: QueryRequest):
    vector_results = query_chunks(request.question, n_results=5)
    keyword_results = query_keywords(request.question, n_results=5)

    vector_documents = vector_results.get("documents", [[]])[0]
    vector_metadatas = vector_results.get("metadatas", [[]])[0]
    vector_ids = vector_results.get("ids", [[]])[0]

    vectors = [
        {
            "id": vector_id,
            "text": document,
            "metadata": metadata,
        }
        for vector_id, document, metadata in zip(vector_ids, vector_documents, vector_metadatas)
    ]

    return _rank_fusion(vectors, keyword_results, limit=5)