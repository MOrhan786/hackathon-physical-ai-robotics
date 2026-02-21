# Implementation Plan: Backend API

**Branch**: `main` | **Date**: 2026-02-19 | **Spec**: `specs/backend-api/spec.md`

## Summary

Build a FastAPI backend with 6 API endpoints: RAG chat (Qdrant + OpenAI), auth (Better Auth + PostgreSQL), content personalization (OpenAI), and Urdu translation (OpenAI). Deploy on HuggingFace Spaces via Docker.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, uvicorn, qdrant-client, openai, psycopg2, better-auth, python-dotenv
**Storage**: PostgreSQL (Neon) for auth, Qdrant Cloud for vectors
**Testing**: Manual API testing (curl/httpie), pytest if time permits
**Target Platform**: HuggingFace Spaces (Docker SDK)
**Project Type**: Backend API service
**Performance Goals**: All endpoints respond within 60s
**Constraints**: HuggingFace free tier (2 vCPU, 16GB RAM), OpenAI rate limits
**Scale/Scope**: Single backend, ~100 concurrent users max

## Constitution Check

| Principle | Status |
|-----------|--------|
| Content-First | PASS — Backend serves content features |
| Jamstack Architecture | PASS — Decoupled API |
| User-Adaptive Learning | PASS — Personalization via background |
| Accessibility | PASS — Urdu translation support |
| Smallest Viable Change | PASS — Minimum endpoints, no over-engineering |
| Security by Default | PASS — .env for secrets, API key validation |

## Project Structure

### Documentation

```text
specs/backend-api/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task breakdown
```

### Source Code

```text
backend/
├── main.py              # FastAPI app entry point + all routes
├── auth.py              # Better Auth integration + user management
├── rag.py               # RAG pipeline: Qdrant search + OpenAI chat
├── ingest.py            # One-time script: chunk docs → embed → store in Qdrant
├── requirements.txt     # Python dependencies
├── Dockerfile           # HuggingFace Spaces Docker deployment
├── .env                 # Environment variables (NOT committed)
├── .env.example         # Template for environment variables
└── README.md            # Backend setup instructions
```

**Structure Decision**: Flat file structure (no nested packages). This is a small backend with 6 endpoints — a single `main.py` with helper modules (`auth.py`, `rag.py`) is the simplest viable approach. No need for `models/`, `services/`, `routers/` directories for this scope.

## Architecture Design

```
                    ┌─────────────────┐
                    │   Frontend      │
                    │   (Vercel)      │
                    └────────┬────────┘
                             │ HTTPS + CORS
                             ▼
┌────────────────────────────────────────────────────┐
│              FastAPI (main.py)                       │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │/api/chat  │  │/api/auth │  │/api/personalize  │  │
│  │          │  │ /signup   │  │/api/translate     │  │
│  └────┬─────┘  │ /signin   │  └────────┬─────────┘  │
│       │        │ /signout  │           │             │
│       │        └─────┬─────┘           │             │
│       ▼              ▼                 ▼             │
│  ┌─────────┐   ┌──────────┐     ┌──────────┐       │
│  │ rag.py  │   │ auth.py  │     │ OpenAI   │       │
│  │         │   │          │     │ Direct   │       │
│  └────┬────┘   └─────┬────┘     └──────────┘       │
│       │              │                               │
└───────┼──────────────┼───────────────────────────────┘
        │              │
        ▼              ▼
  ┌──────────┐   ┌──────────────┐
  │ Qdrant   │   │ PostgreSQL   │
  │ Cloud    │   │ (Neon)       │
  │ Vectors  │   │ Users/Auth   │
  └──────────┘   └──────────────┘
```

## API Contract Summary

### POST /api/chat
```json
// Request
{
  "message": "What is ROS 2?",
  "history": [{"user_message": "...", "ai_response": "..."}],
  "selected_text": "optional context"
}
// Response
{"response": "ROS 2 is..."}
```

### POST /api/auth/signup
```json
// Request
{
  "email": "user@example.com",
  "password": "Password123",
  "name": "User Name",
  "background": {
    "programming_experience": "beginner",
    "robotics_experience": "none",
    "preferred_languages": ["Python"],
    "hardware_access": ["Raspberry Pi"]
  }
}
// Response
{
  "user": {"id": "uuid", "email": "...", "name": "...", "background": {...}},
  "session_token": "token-string"
}
```

### POST /api/auth/signin
```json
// Request
{"email": "user@example.com", "password": "Password123"}
// Response
{"user": {...}, "session_token": "..."}
```

### POST /api/auth/signout
```
// Query param: ?session_token=xxx
// Response
{"message": "Signed out successfully"}
```

### POST /api/personalize
```json
// Request
{
  "content": "Chapter text...",
  "user_background": {"programming_experience": "beginner", ...}
}
// Response
{"personalized_content": "Adapted content..."}
```

### POST /api/translate
```json
// Request
{"content": "Chapter text...", "target_language": "urdu"}
// Response
{"translated_content": "اردو متن..."}
```

## Key Implementation Decisions

### 1. Auth: Better Auth vs Custom
**Decision**: Use Better Auth Python SDK for session-based auth as required by hackathon PDF.
**Fallback**: If Better Auth Python SDK is not mature enough, implement compatible session-based auth with bcrypt + PostgreSQL that matches Better Auth's API contract.

### 2. RAG Pipeline
**Decision**: Simple RAG — embed query → search Qdrant → inject top-5 chunks as context → OpenAI completion.
**Embedding Model**: `text-embedding-3-small` (1536 dimensions, cost-effective)
**Chat Model**: `gpt-4o-mini` (fast, cheap, good quality)
**Chunk Size**: ~500 tokens with 50 token overlap

### 3. Ingestion Strategy
**Decision**: One-time script (`ingest.py`) that:
1. Reads all markdown files from `docs/` folder
2. Splits into chunks (500 tokens, 50 overlap)
3. Embeds each chunk with OpenAI
4. Upserts into Qdrant collection `hackthaon-1-c`
5. Stores metadata: source file, week number, module, heading

### 4. HuggingFace Deployment
**Decision**: Docker-based Space (not Gradio SDK) for full FastAPI control.
**Port**: 7860 (HuggingFace default)
**Dockerfile**: Multi-stage, Python 3.11-slim base

## Complexity Tracking

No constitution violations. All decisions follow smallest-viable-change principle.
