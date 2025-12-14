# Data Model: Gemini API Migration

**Feature**: `003-gemini-api-migration`
**Date**: 2024-12-19

## Overview

This document describes the data models affected by the Gemini API migration. The migration primarily affects the embedding dimensions and API request/response formats, while preserving the external API interface.

## Embedding Model Changes

### Before (OpenAI)

```python
# OpenAI text-embedding-3-small
{
    "model": "text-embedding-3-small",
    "dimensions": 1536,
    "input_format": "string",
    "output_format": "list[float]"
}
```

### After (Gemini)

```python
# Gemini text-embedding-004
{
    "model": "models/text-embedding-004",
    "dimensions": 768,
    "input_format": "string",
    "output_format": "list[float]",
    "task_type": "retrieval_document | retrieval_query"
}
```

### Impact on Qdrant

The Qdrant collection must be recreated with the new dimension:

```python
# Before
collection_config = {
    "vectors": {
        "size": 1536,
        "distance": "Cosine"
    }
}

# After
collection_config = {
    "vectors": {
        "size": 768,
        "distance": "Cosine"
    }
}
```

**Action Required**: Re-ingest all documents after migration.

## Chat Request/Response Models

### ChatRequest (Unchanged)

```python
class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []
    selected_text: Optional[str] = None
```

### Internal History Format

```python
# OpenAI format
history = [
    {"role": "user", "content": "message"},
    {"role": "assistant", "content": "response"}
]

# Gemini format (internal)
history = [
    {"role": "user", "parts": ["message"]},
    {"role": "model", "parts": ["response"]}
]
```

**Note**: The external API format remains unchanged. Conversion happens internally in `GeminiTextbookAgent`.

## Configuration Model

### Before

```python
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    QDRANT_URL: str
    QDRANT_API_KEY: str
    NEON_DB_URL: str
    API_KEY: str
```

### After

```python
class Settings(BaseSettings):
    GEMINI_API_KEY: str  # Changed
    QDRANT_URL: str
    QDRANT_API_KEY: str
    NEON_DB_URL: str
    API_KEY: str
```

## Service Interfaces

### EmbeddingService

```python
class EmbeddingService:
    """Interface unchanged, implementation updated."""
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the given text.
        
        Args:
            text: Input text to embed
            
        Returns:
            768-dimensional embedding vector (was 1536)
        """
        pass
```

### GeminiTextbookAgent (New)

```python
class GeminiTextbookAgent:
    """New agent class for Gemini-based chat."""
    
    async def chat_stream(
        self,
        user_message: str,
        history: List[Dict[str, str]],
        selected_text: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response from the Gemini agent.
        
        Args:
            user_message: The user's question
            history: Previous conversation turns
            selected_text: Optional text selected by user
            
        Yields:
            Response chunks as strings
        """
        pass
```

## Database Schema (Unchanged)

The Neon Postgres schema remains unchanged:

```sql
CREATE TABLE chat_history (
    id SERIAL PRIMARY KEY,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    source_documents JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Contracts (Unchanged)

All external API contracts remain unchanged:

| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| /api/chat | POST | ChatRequest | SSE Stream |
| /api/ingest | POST | - | JSON |
| /api/personalize | POST | PersonalizeRequest | JSON |
| /api/translate | POST | TranslateRequest | JSON |

## Migration Checklist

- [ ] Update Qdrant collection dimensions (1536 → 768)
- [ ] Re-ingest all documents with new embeddings
- [ ] Verify embedding search quality
- [ ] Test chat response quality
- [ ] Validate streaming format compatibility
