# Implementation Plan: Gemini API Migration

**Branch**: `003-gemini-api-migration` | **Date**: 2024-12-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-gemini-api-migration/spec.md`

## Summary

This plan outlines the technical implementation for migrating the RAG Chatbot Backend from OpenAI API to Google Gemini API. The migration involves replacing the OpenAI SDK with Google's Generative AI SDK while maintaining the same external API interface for frontend compatibility.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: FastAPI, google-generativeai, Qdrant-client, Psycopg2, Pydantic
**Storage**: Neon Serverless Postgres (for logging), Qdrant Cloud (for vectors)
**Target Platform**: Local development / Docker container
**Performance Goals**: `< 5 seconds` for chat endpoint to begin streaming
**Constraints**: Must maintain same API interface; must use Gemini API exclusively
**Scale/Scope**: Same as existing system (~100 markdown files, moderate concurrent users)

## Constitution Check

*Initial Check*: Migration adheres to project principles - using environment variables for secrets, maintaining existing interfaces, and following established patterns.

*Post-Design Check*: The migration preserves all existing functionality while swapping the underlying LLM provider.

## Architecture Decision

### ADR: Gemini API Migration

**Context**: The project requires an LLM API for chat completions and embeddings. OpenAI API key is not available.

**Decision**: Migrate to Google Gemini API (gemini-1.5-flash for chat, text-embedding-004 for embeddings).

**Rationale**:
- Available API key (GEMINI_API_KEY)
- Similar functionality to OpenAI (chat completions, embeddings, streaming)
- Good performance for educational content
- Built-in function calling support

**Consequences**:
- Different API interface requires code changes
- Embedding dimensions may differ (requires Qdrant reindexing)
- Response style may vary from GPT-4o

## Migration Strategy

### Phase 1: Dependency Updates
1. Replace `openai` package with `google-generativeai`
2. Update requirements.txt

### Phase 2: Configuration Updates
1. Replace `OPENAI_API_KEY` with `GEMINI_API_KEY` in config
2. Update .env files

### Phase 3: Service Layer Updates
1. Create new GeminiTextbookAgent service
2. Update EmbeddingService for Gemini
3. Update content API endpoints

### Phase 4: Integration & Testing
1. Test all endpoints
2. Re-ingest documents with new embeddings
3. Validate frontend compatibility

## File Changes

### Modified Files

| File | Change Description |
|------|-------------------|
| `rag_chatbot/requirements.txt` | Replace openai with google-generativeai |
| `rag_chatbot/src/core/config.py` | OPENAI_API_KEY → GEMINI_API_KEY |
| `rag_chatbot/src/services/embedding_service.py` | Use Gemini text-embedding-004 |
| `rag_chatbot/src/api/chat.py` | Import GeminiTextbookAgent |
| `rag_chatbot/src/api/content.py` | Use Gemini for personalization/translation |
| `rag_chatbot/.env` | Update environment variable |

### New Files

| File | Description |
|------|-------------|
| `rag_chatbot/src/services/gemini_agent_service.py` | New Gemini-based chat agent |

### Preserved Files (No Changes)

| File | Reason |
|------|--------|
| `rag_chatbot/src/models/chat.py` | API models unchanged |
| `rag_chatbot/src/api/security.py` | Authentication unchanged |
| `rag_chatbot/src/services/db_service.py` | Logging unchanged |
| `rag_chatbot/src/services/vector_store_service.py` | Qdrant interface unchanged |

## API Compatibility Matrix

| Endpoint | Request Format | Response Format | Status |
|----------|---------------|-----------------|--------|
| POST /api/chat | Unchanged | Unchanged (SSE) | ✅ Compatible |
| POST /api/ingest | Unchanged | Unchanged | ✅ Compatible |
| POST /api/personalize | Unchanged | Unchanged | ✅ Compatible |
| POST /api/translate | Unchanged | Unchanged | ✅ Compatible |

## Risk Analysis

### Risk 1: Embedding Dimension Mismatch
- **Impact**: High - existing vectors incompatible
- **Mitigation**: Re-ingest all documents after migration
- **Detection**: Query failures in Qdrant

### Risk 2: Response Quality Difference
- **Impact**: Medium - user experience may vary
- **Mitigation**: Test with sample questions, adjust prompts if needed
- **Detection**: User feedback, quality comparison

### Risk 3: Streaming Format Differences
- **Impact**: Medium - frontend may not parse correctly
- **Mitigation**: Maintain same SSE format, test with frontend
- **Detection**: Frontend integration testing

## Validation Checklist

- [ ] Backend starts with GEMINI_API_KEY
- [ ] Chat endpoint streams responses
- [ ] Personalization works with user backgrounds
- [ ] Translation produces Urdu output
- [ ] Document ingestion creates embeddings
- [ ] Chat history logged to Postgres
- [ ] Frontend integration works
