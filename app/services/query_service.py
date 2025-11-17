from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Qdrant
from app.utils.embedding import get_embedding_model
from app.utils.llm import get_llm_model
from app.config import settings
from qdrant_client import QdrantClient
import logging

logger = logging.getLogger(__name__)

# Initialize Qdrant client
qdrant_client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
    api_key=settings.QDRANT_API_KEY,
    https=settings.QDRANT_HTTPS
)


def query_document(client_id: str, query: str, embedding_model_name: str, llm_model_name: str) -> dict:
    """
    Query the documents of a client: retrieve relevant chunks from Qdrant and get answer from LLM.
    """
    try:
        collection_name = f"{client_id}_{embedding_model_name.replace('/', '_')}"
        logger.info(f"Querying collection: {collection_name}")

        # 1️ Check if collection exists
        try:
            collections = qdrant_client.get_collections()
            collection_names = [c.name for c in collections.collections]
            if collection_name not in collection_names:
                raise ValueError(f"Collection '{collection_name}' not found. Please ingest documents first.")
        except Exception as e:
            raise ValueError(f"Error accessing Qdrant collections: {str(e)}")

        # 2️ Load embedding and LLM models
        embedding_model = get_embedding_model(embedding_model_name)
        llm_model = get_llm_model(llm_model_name)

        # 3️ Initialize vectorstore with Qdrant
        vectorstore = Qdrant(
            client=qdrant_client,
            collection_name=collection_name,
            embeddings=embedding_model
        )

        # 4️ Create RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm_model,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )

        # 5️ Run query
        answer = qa_chain.run(query)

        # 6️ Return structured result
        return {
            "answer": answer,
            "model_used": {
                "embedding_model": embedding_model_name,
                "llm_model": llm_model_name
            }
        }
    
    except Exception as e:
        logger.error(f"Error in query_document: {str(e)}")
        raise
