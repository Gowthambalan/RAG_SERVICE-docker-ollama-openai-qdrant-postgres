from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient as QdrantDBClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.utils.embedding import get_embedding_model
from app.utils.pdf_parser import extract_text_from_pdf
from app.config import settings

# Initialize Qdrant client
qdrant_client = QdrantDBClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    api_key=settings.QDRANT_API_KEY,
    https=settings.QDRANT_HTTPS
)


def ingest_document(client_id: str, document_id: str, file_path: str, embedding_model_name: str) -> dict:
    """
    Ingest a PDF document: extract text, create embeddings, and store in Qdrant.
    """
    # 1️ Extract text from PDF
    text = extract_text_from_pdf(file_path)
    if not text.strip():
        raise ValueError(f"No text extracted from file '{file_path}'")

    # 2️ Get embedding model
    embedding_model = get_embedding_model(embedding_model_name)

    # 3️ Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text)
    if not chunks:
        raise ValueError(f"No text chunks generated from '{file_path}'")

    # 4️ Determine collection name
    collection_name = f"{client_id}_{embedding_model_name.replace('/', '_')}"

    # 5️ Determine embedding vector size
    test_vector = embedding_model.embed_query("test")
    vector_size = len(test_vector)

    # 6️ Create collection if it doesn't exist
    existing_collections = [c.name for c in qdrant_client.get_collections().collections]
    if collection_name not in existing_collections:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    # 7️ Store chunks in Qdrant - CORRECTED
    store = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embedding_model  #  Fixed parameter name
    )
    
    store.add_texts(
        texts=chunks,
        metadatas=[{"document_id": document_id, "chunk_id": i} for i in range(len(chunks))]
    )

    # 8️ Return summary
    return {
        "status": "success",
        "document_id": document_id,
        "collection": collection_name,
        "chunks_stored": len(chunks),
        "message": f"Document stored in '{collection_name}' using {client_id}'s embedding model."
    }
