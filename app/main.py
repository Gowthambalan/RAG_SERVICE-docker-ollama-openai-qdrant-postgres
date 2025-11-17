from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db, Base, engine
from app.schemas import SetModelsRequest, UpdateModelsRequest, IngestRequest, QueryRequest
from app.services.client_service import set_client_models, get_client, update_client_models
from app.services.ingestion_service import ingest_document
from app.services.query_service import query_document

# Ensure tables are created on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Service-based RAG System", version="1.0.0")


@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "ok", "message": "RAG service is up and running"}


@app.post("/set_models")
def set_models(req: SetModelsRequest, db: Session = Depends(get_db)):
    """Set embedding and LLM models for a client."""
    client = set_client_models(db, req.client_id, req.embedding_model, req.llm_model)
    return {
        "status": "success",
        "client_id": client.client_id,
        "embedding_model": client.embedding_model,
        "llm_model": client.llm_model,
        "message": f"Models set successfully for client {client.client_id}.",
    }


@app.post("/update_set_models")
def update_models(req: UpdateModelsRequest, db: Session = Depends(get_db)):
    """Update a client’s model settings."""
    try:
        client = update_client_models(db, req.client_id, req.embedding_model, req.llm_model)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {
        "status": "success",
        "client_id": client.client_id,
        "embedding_model": client.embedding_model,
        "llm_model": client.llm_model,
        "message": f"Models updated successfully for client {client.client_id}.",
    }

from fastapi import UploadFile, File

@app.post("/ingest_file")
def ingest_file(
    client_id: str,
    document_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF file and ingest it into Qdrant using the client's embedding model.
    """
    # 1️ Get client info from DB
    client = get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # 2️ Save uploaded file temporarily
    file_location = f"/tmp/{file.filename}"
    try:
        with open(file_location, "wb") as f:
            f.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {str(e)}")

    # 3️ Call ingest_document with the corrected Qdrant API
    try:
        result = ingest_document(
            client_id=client.client_id,
            document_id=document_id,
            file_path=file_location,
            embedding_model_name=client.embedding_model
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    return result


@app.post("/query")
def query(req: QueryRequest, db: Session = Depends(get_db)):
    """Run a query against the ingested documents for a client."""
    client = get_client(db, req.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        result = query_document(
            client_id=client.client_id,
            query=req.query,
            embedding_model_name=client.embedding_model,
            llm_model_name=client.llm_model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

    return {"status": "success", "result": result}
