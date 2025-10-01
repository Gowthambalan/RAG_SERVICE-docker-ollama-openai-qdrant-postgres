# test_connection.py
import requests
from app.config import settings

def test_ollama_connection():
    try:
        # Test Ollama connection
        response = requests.get(f"{settings.ollama_url}/api/tags", timeout=10)
        print(f"Ollama connection: {response.status_code}")
        print(f"Available models: {response.json()}")
        
        # Test with the specific model
        generate_data = {
            "model": settings.LLM_QWEN,
            "prompt": "Hello, test message",
            "stream": False
        }
        response = requests.post(
            f"{settings.ollama_url}/api/generate",
            json=generate_data,
            timeout=30
        )
        print(f"Model test: {response.status_code}")
        if response.status_code == 200:
            print("✅ Model is working!")
        else:
            print(f"❌ Model error: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_ollama_connection()