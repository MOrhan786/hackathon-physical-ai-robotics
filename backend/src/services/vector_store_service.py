from qdrant_client import QdrantClient, models
from typing import List, Dict
import hashlib

from src.core.config import settings

class VectorStoreService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
        self.collection_name = "textbook_embeddings"
        self.vector_size = 768  # For Gemini text-embedding-001

    def recreate_collection(self):
        """Deletes and recreates the collection."""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE),
        )

    def upsert_vectors(self, chunks: List[Dict[str, str]], embeddings: List[List[float]]):
        """Upserts vectors and their payloads to the Qdrant collection."""
        points = []
        for i, chunk in enumerate(chunks):
            points.append(
                models.PointStruct(
                    id=hash(chunk["chunk_hash"]) % (10**9),  # Simple way to get int ID from hash
                    vector=embeddings[i],
                    payload={
                        "text": chunk["content"],
                        "source_file": chunk["source_file"],
                        "chunk_hash": chunk["chunk_hash"],
                    },
                )
            )
        
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            wait=True,
            points=points,
        )
        return operation_info

    def search_vectors(self, query_embedding: List[float], limit: int = 5) -> List[Dict]:
        """Searches for similar vectors in the collection using query_points API."""
        try:
            # Use query_points (new API in qdrant-client 1.7+)
            response = self.client.query_points(
                collection_name=self.collection_name,
                query=query_embedding,
                limit=limit,
                with_payload=True,
            )
            results = []
            for point in response.points:
                results.append({
                    "score": point.score,
                    "text": point.payload.get("text"),
                    "source_file": point.payload.get("source_file"),
                })
            return results
        except Exception as e:
            print(f"Error searching vectors: {e}")
            return []

if __name__ == "__main__":
    # Example usage (requires QDRANT_URL and QDRANT_API_KEY in .env)
    # AND a running Qdrant instance
    # AND OPENAI_API_KEY for embedding service to generate test embeddings
    from embedding_service import EmbeddingService # Assuming it's in the same directory

    vector_store_service = VectorStoreService()
    embedding_service = EmbeddingService()

    # Create dummy chunks and embeddings
    test_chunks = [
        {"content": "Physics is the natural science that studies matter, its fundamental constituents, its motion and behavior through space and time, and the related entities of energy and force.", "source_file": "physics.md", "chunk_hash": hashlib.md5("Physics is the natural science...".encode()).hexdigest()},
        {"content": "Quantum mechanics is a fundamental theory in physics that describes the behaviors of nature at the smallest scales of energy levels of atoms and subatomic particles.", "source_file": "quantum.md", "chunk_hash": hashlib.md5("Quantum mechanics is a fundamental theory...".encode()).hexdigest()},
        {"content": "Classical mechanics is a physical theory describing the motion of macroscopic objects, from projectiles to parts of machinery, and astronomical objects, such as spacecraft, planets, stars, and galaxies.", "source_file": "classical.md", "chunk_hash": hashlib.md5("Classical mechanics is a physical theory...".encode()).hexdigest()},
    ]
    test_texts = [chunk["content"] for chunk in test_chunks]
    test_embeddings = embedding_service.get_embeddings(test_texts)

    print("Recreating Qdrant collection...")
    vector_store_service.recreate_collection()
    print("Upserting vectors...")
    upsert_result = vector_store_service.upsert_vectors(test_chunks, test_embeddings)
    print(f"Upsert operation status: {upsert_result}")

    # Test search
    query_text = "What is the study of matter and energy?"
    query_embedding = embedding_service.get_embedding(query_text)
    print(f"\nSearching for: '{query_text}'")
    search_results = vector_store_service.search_vectors(query_embedding)
    print("Search results:")
    for res in search_results:
        print(f"  Score: {res['score']:.4f}, Source: {res['source_file']}, Text: {res['text'][:50]}...")
