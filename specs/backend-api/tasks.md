# Implementation Tasks: Backend API

**Date**: 2026-02-19 | **Spec**: `specs/backend-api/spec.md` | **Plan**: `specs/backend-api/plan.md`

---

## Task 1: Project Setup & Dependencies (P0) - DONE
**Depends on**: Nothing
**Files**: `backend/requirements.txt`, `backend/.env`, `backend/.env.example`

- [x] Create `backend/` directory
- [x] Create `requirements.txt` with: fastapi, uvicorn, qdrant-client, openai, psycopg2-binary, python-dotenv, bcrypt, pydantic, python-multipart
- [x] Create `.env` with all credentials (DB, Qdrant, OpenAI, Better Auth)
- [x] Create `.env.example` with placeholder values
- [x] Verify all dependencies install correctly

**Test**: `pip install -r requirements.txt` succeeds - PASSED

---

## Task 2: FastAPI App Skeleton (P0) - DONE
**Depends on**: Task 1
**Files**: `backend/main.py`

- [x] Create FastAPI app with CORS middleware (allow Vercel + localhost)
- [x] Add X-API-Key validation middleware
- [x] Define all Pydantic request/response models
- [x] Create all 6 route endpoints (fully implemented, not stubs)
- [x] Add health check endpoint `GET /`
- [x] Run with uvicorn on port 7860

**Test**: `curl http://localhost:7860/` returns health check - PASSED

---

## Task 3: PostgreSQL Auth Module (P1) - DONE
**Depends on**: Task 2
**Files**: `backend/auth.py`

- [x] Connect to Neon PostgreSQL
- [x] Create users table (id, email, name, password_hash, background JSON, created_at)
- [x] Create sessions table (id, user_id, token, expires_at, created_at)
- [x] Auto-create tables on startup if not exist
- [x] Implement signup: validate -> hash password -> insert user -> create session -> return token
- [x] Implement signin: find user -> verify password -> create session -> return token
- [x] Implement signout: delete session by token
- [x] Wire auth endpoints in main.py
- [x] Verify tables show in Neon dashboard

**Test**: Signup -> Signin -> Signout flow works via curl - PASSED

---

## Task 4: Qdrant Ingestion Script (P1) - DONE
**Depends on**: Task 1
**Files**: `backend/ingest.py`

- [x] Connect to Qdrant Cloud
- [x] Read all markdown files from `docs/` directory
- [x] Parse markdown: extract headings, content sections
- [x] Chunk text with overlapping windows
- [x] Generate embeddings with OpenAI text-embedding-3-small
- [x] Upsert chunks into Qdrant collection `hackthaon-1-c` with metadata
- [x] Handle existing collection (recreate)
- [x] Print progress and final count
- [x] 3712 chunks successfully ingested

**Test**: Run script -> Query Qdrant -> Returns relevant chunks for "ROS 2" - PASSED (score 0.69)

---

## Task 5: RAG Chat Endpoint (P1) - DONE
**Depends on**: Task 4
**Files**: `backend/rag.py`, `backend/main.py`

- [x] Connect to Qdrant Cloud
- [x] Embed user query with OpenAI
- [x] Search Qdrant for top-5 similar chunks
- [x] Build prompt: system message + retrieved chunks + chat history + user message
- [x] Call OpenAI gpt-4o-mini for completion
- [x] Handle selected_text as additional context
- [x] Return response
- [x] Wire `/api/chat` endpoint in main.py

**Test**: POST `/api/chat` with "What is ROS 2?" -> Returns textbook-grounded answer - PASSED

---

## Task 6: Personalization Endpoint (P2) - DONE
**Depends on**: Task 2
**Files**: `backend/main.py`, `backend/rag.py`

- [x] Receive content + user_background
- [x] Build OpenAI prompt for level-appropriate rewriting
- [x] Call OpenAI gpt-4o-mini
- [x] Return personalized_content

**Test**: POST `/api/personalize` with beginner background -> Simpler content returned - PASSED

---

## Task 7: Translation Endpoint (P2) - DONE
**Depends on**: Task 2
**Files**: `backend/main.py`, `backend/rag.py`

- [x] Receive content + target_language
- [x] Build OpenAI prompt: "Translate to Urdu. Keep code blocks in English."
- [x] Call OpenAI gpt-4o-mini
- [x] Return translated_content

**Test**: POST `/api/translate` with English text -> Urdu text returned - PASSED

---

## Task 8: Dockerfile & HuggingFace Deploy (P1) - DONE
**Depends on**: Tasks 2-7
**Files**: `backend/Dockerfile`, `backend/README.md`

- [x] Create Dockerfile (python:3.11-slim, install deps, copy code, CMD uvicorn)
- [x] Expose port 7860 (HuggingFace default)
- [x] Create README.md for HuggingFace Space
- [x] Deploy to HuggingFace Spaces (MrsAsif/hackathon1-c)
- [x] Set all 6 environment secrets via HF API
- [x] Verify all endpoints work on https://mrsasif-hackathon1-c.hf.space

**Test**: All endpoints work on HuggingFace Space - PASSED

---

## Task 9: Update Frontend API URLs (P1) - DONE
**Depends on**: Task 8
**Files**: `src/config.ts`, `src/components/AuthContext.tsx`, `src/components/Chat/ChatPanel.tsx`, `src/theme/DocItem/Personalizer.tsx`, `src/theme/DocItem/TranslationControl.tsx`, `docusaurus.config.ts`

- [x] Update all API URLs to HuggingFace Space URL (`https://mrsasif-hackathon1-c.hf.space`)
- [x] Update `src/config.ts` (central config + static exports)
- [x] Update `src/components/AuthContext.tsx` (auth API calls)
- [x] Update `src/components/Chat/ChatPanel.tsx` (RAG chat)
- [x] Update `src/theme/DocItem/Personalizer.tsx` (personalization)
- [x] Update `src/theme/DocItem/TranslationControl.tsx` (translation)
- [x] Update `docusaurus.config.ts` customFields
- [x] Frontend builds successfully with new URLs

**Test**: Frontend build succeeds with updated URLs - PASSED

---

## Execution Summary

| Task | Status | Test |
|------|--------|------|
| 1. Project Setup | DONE | PASSED |
| 2. FastAPI Skeleton | DONE | PASSED |
| 3. PostgreSQL Auth | DONE | PASSED |
| 4. Qdrant Ingestion | DONE | PASSED |
| 5. RAG Chat | DONE | PASSED |
| 6. Personalization | DONE | PASSED |
| 7. Translation | DONE | PASSED |
| 8. Docker/Deploy | DONE | PASSED |
| 9. Frontend URLs | DONE | PASSED |

**9/9 tasks complete. All backend tasks DONE!**
