from pydantic import BaseModel
from fastapi import APIRouter

from app.retrieval.bm25_store import query_keywords

router = APIRouter()


class KeywordRequest(BaseModel):
    question: str


@router.post("/keyword")
def keyword_search(request: KeywordRequest):
    return query_keywords(request.question, n_results=5)