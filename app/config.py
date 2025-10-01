from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_HTTPS: bool = False
    QDRANT_API_KEY: str

    # LLM Models
    LLM_QWEN: str
    LLM_OPENAI: str

    # Embedding Models
    EMB_OPENAI: str
    EMB_SENTENCE_TRANSFORMER: str

    # API Keys
    OPENAI_API_KEY: str

    # Ollama Configuration
    LLM_HOST: str = "localhost"
    LLM_PORT: int = 11434

    @property
    def database_url(self) -> str:
        """Return SQLAlchemy Postgres connection URL"""
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def qdrant_url(self) -> str:
        """Return Qdrant HTTP endpoint URL"""
        protocol = "https" if self.QDRANT_HTTPS else "http"
        return f"{protocol}://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    @property
    def ollama_url(self) -> str:
        """Return Ollama HTTP endpoint URL"""
        return f"http://{self.LLM_HOST}:{self.LLM_PORT}"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()