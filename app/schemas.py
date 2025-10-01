from pydantic import BaseModel


class SetModelsRequest(BaseModel):
    client_id: str
    embedding_model: str
    llm_model: str


class UpdateModelsRequest(BaseModel):
    client_id: str
    embedding_model: str | None = None
    llm_model: str | None = None


class IngestRequest(BaseModel):
    client_id: str
    document_id: str
    file_path: str


class QueryRequest(BaseModel):
    client_id: str
    query: str
