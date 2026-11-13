from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, HnswConfigDiff
from smart_support_agent.config import settings
from smart_support_agent.services.embeddings import embedding_service
from smart_support_agent.schemas import Passage


class QdrantService:
    def __init__(self):
        if settings.USE_LOCAL_QDRANT:
            self.client = QdrantClient(path=settings.QDRANT_PATH)
        else:
            self.client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

        self.collection_name = settings.QDRANT_COLLECTION
        self._ensure_collection()

    def _ensure_collection(self):
        collections = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in collections:
            vector_size = embedding_service.model.get_sentence_embedding_dimension()

            # Creating collection with explicit HNSW (ANN) configuration
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                    # Explicitly tuning HNSW for ANN search performance
                    hnsw_config=HnswConfigDiff(
                        m=16,  # Number of edges per node in the graph (default is 16)
                        ef_construct=100,
                        # Size of the dynamic list during index construction (higher = better accuracy, slower indexing)
                        full_scan_threshold=10000  # Switch to HNSW search automatically
                    )
                ),
            )

    def upsert_chunks(self, chunks: list[dict]) -> int:
        texts = [c["text"] for c in chunks]
        vectors = embedding_service.generate_embeddings(texts)

        points = []
        for idx, (chunk, vector) in enumerate(zip(chunks, vectors)):
            point_id = hash(f"{chunk['doc_id']}_{idx}") & 0xFFFFFFFFFFFFFFFF
            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "doc_id": chunk["doc_id"],
                        "text": chunk["text"],
                        "source": chunk["source"],
                        "section": chunk["section"]
                    }
                )
            )

        self.client.upsert(collection_name=self.collection_name, points=points)
        return len(points)

    def search_similar(self, query: str, top_k: int = 6) -> list[Passage]:
        query_vector = embedding_service.generate_query_embedding(query)

        # Using query_points for robust compatibility across client versions
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
        ).points

        passages = []
        for hit in search_result:
            passages.append(
                Passage(
                    text=hit.payload.get("text", ""),
                    source=hit.payload.get("source", ""),
                    section=hit.payload.get("section", ""),
                    score=float(hit.score)
                )
            )
        return passages


qdrant_service = QdrantService()