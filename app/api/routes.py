from fastapi import APIRouter
from app.api.schemas import QueryRequest, QueryResponse
from app.rag.pipeline import rag_pipeline

router = APIRouter()

@router.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    result = rag_pipeline(request.query, request.role)
    return result