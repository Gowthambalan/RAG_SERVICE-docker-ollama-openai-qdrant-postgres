from langchain_community.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings
from app.config import settings

def get_embedding_model(name: str):
    """
    Return the embedding model instance based on the provided name.
    """
    if name == settings.EMB_OPENAI:
        return OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    elif name == settings.EMB_SENTENCE_TRANSFORMER:
        return SentenceTransformerEmbeddings(model_name=settings.EMB_SENTENCE_TRANSFORMER)
    else:
        raise ValueError(f"Invalid embedding model name: '{name}'")