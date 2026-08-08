from fastapi import APIRouter, Query

from app.retrieval.chroma_store import query_chunks

router = APIRouter()


@router.get("/retrieve")
def retrieve_chunks(q: str = Query(...), n_results: int = 3):
    results = query_chunks(q, n_results=n_results)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    return {
        "query": q,
        "results": [
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
            for document, metadata, distance in zip(documents, metadatas, distances)
        ],
    }