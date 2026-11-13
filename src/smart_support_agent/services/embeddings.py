from sentence_transformers import SentenceTransformer
from smart_support_agent.config import settings


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def generate_query_embedding(self, query: str) -> list[float]:
        embedding = self.model.encode(query, show_progress_bar=False)
        return embedding.tolist()


embedding_service = EmbeddingService()