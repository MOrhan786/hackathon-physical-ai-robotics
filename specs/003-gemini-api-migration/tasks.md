# Tasks: Gemini API Migration

This document outlines the development tasks for migrating from OpenAI API to Google Gemini API.

**Feature**: `003-gemini-api-migration`
**Spec**: [`specs/003-gemini-api-migration/spec.md`](./spec.md)
**Plan**: [`specs/003-gemini-api-migration/plan.md`](./plan.md)

## Implementation Strategy

The migration proceeds in phases to minimize risk and ensure each component works before moving to the next.

1. **Phase 1 (Dependencies)**: Update package dependencies
2. **Phase 2 (Configuration)**: Update environment configuration
3. **Phase 3 (Services)**: Migrate service layer to Gemini
4. **Phase 4 (Validation)**: Test and validate all functionality

## Phase 1: Dependencies

- [x] T001 Update `rag_chatbot/requirements.txt` to replace `openai>=1.12.0` with `google-generativeai>=0.8.0`
- [x] T002 Install the new google-generativeai package

## Phase 2: Configuration

- [x] T003 Update `rag_chatbot/src/core/config.py` to use `GEMINI_API_KEY` instead of `OPENAI_API_KEY`
- [x] T004 Update `rag_chatbot/.env` with `GEMINI_API_KEY` placeholder
- [x] T005 Update `rag_chatbot/.env.example` with new environment variable

## Phase 3: Service Layer Migration

### Embedding Service
- [x] T006 [US2] Update `rag_chatbot/src/services/embedding_service.py` to use Gemini's text-embedding-004 model
  - Replace OpenAI client with genai.configure()
  - Use genai.embed_content() for embedding generation
  - Maintain same interface (get_embedding method)

### Chat Agent Service
- [x] T007 [US1] Create new `rag_chatbot/src/services/gemini_agent_service.py` with GeminiTextbookAgent class
  - Initialize Gemini model (gemini-1.5-flash)
  - Implement _search_textbook method for RAG retrieval
  - Implement chat_stream async generator for streaming responses
  - Support conversation history
  - Support selected_text context prioritization

### API Endpoints
- [x] T008 [US1] Update `rag_chatbot/src/api/chat.py` to import and use gemini_textbook_agent
- [x] T009 [US3,US4] Update `rag_chatbot/src/api/content.py` to use Gemini for personalization and translation
  - Replace OpenAI client with Gemini model
  - Update generate_content calls with proper configuration

## Phase 4: Documentation & Validation

### Documentation
- [x] T010 Update `README.md` to reflect Gemini API usage
- [x] T013 Create ADR for Gemini API migration decision
- [x] T014 Create PHR for implementation session
- [x] T015 Create implementation checklist

### Validation
- [x] T016 Verify backend starts successfully with Gemini API
- [ ] T017 Test chat endpoint with sample questions
- [ ] T018 Test personalization endpoint with user backgrounds
- [ ] T019 Test translation endpoint for Urdu output
- [ ] T020 Re-ingest documents with Gemini embeddings
- [ ] T021 Verify frontend integration works

## Dependencies

- **T006-T009** depend on **T001-T005**: Services need dependencies and config first
- **T016-T021** depend on **T006-T009**: Validation needs services implemented

## Completion Status

| Phase | Status | Tasks Completed |
|-------|--------|-----------------|
| Phase 1 | ✅ Complete | T001-T002 |
| Phase 2 | ✅ Complete | T003-T005 |
| Phase 3 | ✅ Complete | T006-T009 |
| Phase 4 | 🔄 In Progress | T010-T016 done, T017-T021 pending |

## Files Modified

- `rag_chatbot/requirements.txt`
- `rag_chatbot/src/core/config.py`
- `rag_chatbot/src/services/embedding_service.py`
- `rag_chatbot/src/services/gemini_agent_service.py` (new)
- `rag_chatbot/src/api/chat.py`
- `rag_chatbot/src/api/content.py`
- `rag_chatbot/.env`
- `README.md`
