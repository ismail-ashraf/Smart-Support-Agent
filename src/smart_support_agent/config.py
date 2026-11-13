from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / ".env"

class Settings(BaseSettings):
    PROJECT_NAME: str
    API_V1_STR: str

    # Qdrant Configuration
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    QDRANT_PATH: str
    USE_LOCAL_QDRANT: bool

    # Embedding Model Configuration
    EMBEDDING_MODEL_NAME: str

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding='utf-8',
        extra="ignore"
    )


settings = Settings()