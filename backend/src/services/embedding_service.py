from openai import OpenAI
from typing import List
from src.core.config import settings

class EmbeddingService:
    """Embedding service using Gemini's OpenAI-compatible endpoint."""
    
    def __init__(self):
        # Use Gemini's OpenAI-compatible endpoint for embeddings
        self.client = OpenAI(
            api_key=settings.GEMINI_API_KEY,
            base_url=settings.GEMINI_BASE_URL
        )
        # Gemini embedding model (text-embedding-004 is the latest available)
        self.embedding_model = "text-embedding-004"

    def get_embedding(self, text: str) -> List[float]:
        text = text.replace("\n", " ")
        response = self.client.embeddings.create(input=[text], model=self.embedding_model)
        return response.data[0].embedding

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        # Replace newlines for better embedding quality
        processed_texts = [text.replace("\n", " ") for text in texts]
        
        # Gemini has a batch limit of 100 requests
        batch_size = 100
        all_embeddings = []
        
        for i in range(0, len(processed_texts), batch_size):
            batch = processed_texts[i:i + batch_size]
            response = self.client.embeddings.create(input=batch, model=self.embedding_model)
            all_embeddings.extend([data.embedding for data in response.data])
        
        return all_embeddings

if __name__ == "__main__":
    # Example usage (requires GEMINI_API_KEY to be set in .env)
    embedding_service = EmbeddingService()
    
    sample_text = "This is a test sentence for embedding."
    embedding = embedding_service.get_embedding(sample_text)
    print(f"Embedding for '{sample_text[:30]}...': {embedding[:5]}...") # Print first 5 elements

    sample_texts = [
        "First sentence to embed.",
        "Second sentence for embedding."
    ]
    embeddings = embedding_service.get_embeddings(sample_texts)
    print(f"\nEmbeddings for multiple texts (first 5 elements of first embedding): {embeddings[0][:5]}...")
