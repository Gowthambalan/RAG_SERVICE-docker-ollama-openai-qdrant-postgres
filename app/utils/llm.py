from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def get_llm_model(name: str):
    """
    Return the LLM model instance based on the provided name.
    Raises ValueError if model name is invalid.
    """
    try:
        if name == settings.LLM_QWEN:
            logger.info(f"Initializing Ollama model: {settings.LLM_QWEN} at {settings.LLM_HOST}:{settings.LLM_PORT}")
            return Ollama(
                model=settings.LLM_QWEN,
                base_url=f"http://{settings.LLM_HOST}:{settings.LLM_PORT}",
                temperature=0.1,
                timeout=120,  # Increased timeout for better reliability
                num_predict=512
            )
        elif name == settings.LLM_OPENAI:
            logger.info(f"Initializing OpenAI model: {settings.LLM_OPENAI}")
            return ChatOpenAI(
                model=settings.LLM_OPENAI,  # Changed from model_name to model
                openai_api_key=settings.OPENAI_API_KEY,
                temperature=0.1
            )
        else:
            raise ValueError(f"Invalid LLM model name: '{name}'")
    except Exception as e:
        logger.error(f"Failed to initialize LLM model '{name}': {str(e)}")
        raise