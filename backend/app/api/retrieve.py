from pydantic import BaseModel
from fastapi import APIRouter

from app.retrieval.chroma_store import query_chunks

router = APIRouter()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def query_documents(request: QueryRequest):
    results = query_chunks(request.question, n_results=5)
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    return [
        {
            "text": document,
            "metadata": metadata,
            "distance": distance,
        }
        for document, metadata, distance in zip(documents, metadatas, distances)
    ]