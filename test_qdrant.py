# test_qdrant.py
from app.config import settings
from qdrant_client import QdrantClient

def test_qdrant():
    try:
        client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            api_key=settings.QDRANT_API_KEY,
            https=settings.QDRANT_HTTPS
        )
        collections = client.get_collections()
        print("✅ Qdrant connection successful")
        print("Available collections:", [c.name for c in collections.collections])
    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")

if __name__ == "__main__":
    test_qdrant()