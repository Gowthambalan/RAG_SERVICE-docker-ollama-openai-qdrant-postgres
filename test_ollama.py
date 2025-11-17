# test_ollama.py
import requests
from app.config import settings

def test_ollama():
    try:
        url = f"http://{settings.LLM_HOST}:{settings.LLM_PORT}/api/tags"
        response = requests.get(url, timeout=10)
        print(f" Ollama connection successful: {response.status_code}")
        print("Available models:", response.json())
    except Exception as e:
        print(f" Ollama connection failed: {e}")

if __name__ == "__main__":
    test_ollama()
