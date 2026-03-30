from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    role: str

class QueryResponse(BaseModel):
    answer: str
    sources: list