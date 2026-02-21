# Feature Specification: Backend API for Physical AI Textbook

**Feature Branch**: `main`
**Created**: 2026-02-19
**Status**: Approved
**Input**: User description: "Backend API with RAG chatbot, authentication (Better Auth), content personalization, Urdu translation. Deploy on HuggingFace Spaces. Use Qdrant for vector DB, PostgreSQL (Neon) for auth DB, OpenAI for LLM."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAG Chat with Textbook Content (Priority: P1)

A student reads a chapter about ROS 2, has a question, types it in the chat widget. The backend receives the message, searches Qdrant for relevant textbook chunks, passes them as context to OpenAI, and returns an accurate answer grounded in the textbook.

**Why this priority**: Core hackathon requirement. The RAG chatbot is the primary interactive feature that differentiates this from a static textbook.

**Independent Test**: Send POST to `/api/chat` with `{"message": "What is ROS 2?"}` — response must contain relevant textbook content about ROS 2.

**Acceptance Scenarios**:

1. **Given** textbook content is indexed in Qdrant, **When** user sends "What is VSLAM?", **Then** response contains accurate VSLAM information from textbook
2. **Given** user selects text on page, **When** user asks "Explain this", **Then** response uses selected_text as additional context
3. **Given** user has chat history, **When** user asks follow-up question, **Then** response considers previous messages for continuity
4. **Given** Qdrant is unreachable, **When** user sends message, **Then** system returns graceful error (not 500 crash)

---

### User Story 2 - User Authentication with Better Auth (Priority: P1)

A new student visits the textbook site, clicks "Sign Up", fills in email/password/name and their background (programming experience, robotics experience, preferred languages, hardware access). The backend creates their account using Better Auth, stores background in PostgreSQL, and returns a session token.

**Why this priority**: Authentication enables personalization and translation (bonus features). Better Auth is specifically required by hackathon PDF.

**Independent Test**: POST to `/api/auth/signup` with valid data → 200 with session token. POST to `/api/auth/signin` with same credentials → 200 with same user data.

**Acceptance Scenarios**:

1. **Given** no account exists, **When** user signs up with email/password/name/background, **Then** account created, session token returned
2. **Given** account exists, **When** user signs in with correct credentials, **Then** session token and user data returned
3. **Given** user is logged in, **When** user calls signout, **Then** session invalidated
4. **Given** email already registered, **When** new signup with same email, **Then** error "Email already in use"
5. **Given** wrong password, **When** user signs in, **Then** error "Invalid credentials"

---

### User Story 3 - Content Personalization (Priority: P2)

A logged-in beginner student opens Week 3 (ROS Fundamentals), presses "Personalize" button. The backend receives the chapter text and the user's background, uses OpenAI to rewrite the content at the appropriate level, and returns personalized HTML.

**Why this priority**: Bonus 50 points in hackathon. Depends on auth (P1).

**Independent Test**: POST to `/api/personalize` with chapter content + beginner background → response has simpler explanations.

**Acceptance Scenarios**:

1. **Given** user is beginner, **When** personalizing a chapter, **Then** content is simplified with more explanations
2. **Given** user is advanced, **When** personalizing a chapter, **Then** content includes deeper technical details
3. **Given** content is very long, **When** personalizing, **Then** response completes within 60s timeout

---

### User Story 4 - Urdu Translation (Priority: P2)

A logged-in student opens any chapter, presses "Translate to Urdu" button. The backend receives the chapter text, uses OpenAI to translate it to Urdu, and returns the translated content.

**Why this priority**: Bonus 50 points in hackathon. Independent of personalization.

**Independent Test**: POST to `/api/translate` with English text + target_language="urdu" → response contains Urdu text.

**Acceptance Scenarios**:

1. **Given** English chapter content, **When** translating to Urdu, **Then** response contains accurate Urdu translation
2. **Given** content has code blocks, **When** translating, **Then** code blocks remain in English, only explanations translated
3. **Given** content is very long, **When** translating, **Then** response completes within 60s timeout

---

### User Story 5 - Textbook Content Ingestion into Qdrant (Priority: P1)

Before the chatbot can work, all 13 weeks of textbook markdown content must be chunked, embedded, and stored in Qdrant vector database. This is a one-time data pipeline.

**Why this priority**: Without indexed content, RAG chat returns empty/hallucinated responses.

**Independent Test**: After ingestion, query Qdrant collection `hackthaon-1-c` → returns relevant chunks for "ROS 2 nodes topics services".

**Acceptance Scenarios**:

1. **Given** 15 markdown docs in `docs/` folder, **When** ingestion script runs, **Then** all content chunked and stored in Qdrant
2. **Given** content is chunked, **When** querying "NVIDIA Isaac Sim", **Then** returns chunks from Week 8-10
3. **Given** chunks exist, **When** querying with embedding, **Then** semantic similarity search works correctly

---

### Edge Cases

- What happens when OpenAI API key is invalid? → Return 503 with "AI service unavailable"
- What happens when Qdrant is down? → Return 503 with "Search service unavailable"
- What happens when request body is malformed? → Return 422 with validation error details
- What happens when session token is expired/invalid? → Return 401 "Unauthorized"
- What happens when content is too long for OpenAI? → Truncate to fit context window
- What happens with concurrent requests? → FastAPI async handles them properly

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST expose REST API with endpoints: `/api/chat`, `/api/personalize`, `/api/translate`, `/api/auth/signup`, `/api/auth/signin`, `/api/auth/signout`
- **FR-002**: System MUST use Qdrant Cloud for vector search (collection: `hackthaon-1-c`, cluster: `rag-chatbot`)
- **FR-003**: System MUST use PostgreSQL (Neon) for user data and Better Auth sessions
- **FR-004**: System MUST use OpenAI API for embeddings, chat completions, personalization, and translation
- **FR-005**: System MUST implement Better Auth for authentication (signup/signin/signout with session tokens)
- **FR-006**: System MUST accept user background at signup: programming_experience, robotics_experience, preferred_languages[], hardware_access[]
- **FR-007**: System MUST support CORS for frontend domains (Vercel deployment + localhost)
- **FR-008**: System MUST validate X-API-Key header on all requests
- **FR-009**: System MUST include an ingestion script to chunk and embed textbook markdown into Qdrant
- **FR-010**: System MUST be deployable on HuggingFace Spaces (Docker or Gradio SDK)
- **FR-011**: System MUST handle chat history for context continuity
- **FR-012**: System MUST handle selected_text as additional context for chat queries

### Key Entities

- **User**: id, email, name, password_hash, background (JSON), created_at
- **Session**: id, user_id, token, expires_at, created_at
- **UserBackground**: programming_experience (enum), robotics_experience (enum), preferred_languages (array), hardware_access (array)
- **ChatRequest**: message (string), history (array), selected_text (optional string)
- **ChatResponse**: response (string)
- **PersonalizeRequest**: content (string), user_background (object)
- **PersonalizeResponse**: personalized_content (string)
- **TranslateRequest**: content (string), target_language (string)
- **TranslateResponse**: translated_content (string)

---

## Technology Stack

| Component | Technology | Details |
|-----------|-----------|---------|
| Framework | FastAPI | Python async web framework |
| Vector DB | Qdrant Cloud | `https://76434cf8-...cloud.qdrant.io` |
| Auth DB | PostgreSQL (Neon) | `ep-gentle-firefly-abls73h2-pooler.eu-west-2.aws.neon.tech` |
| Auth Library | Better Auth (Python) | Session-based auth |
| LLM | OpenAI GPT-4o-mini | Chat, personalization, translation |
| Embeddings | OpenAI text-embedding-3-small | For Qdrant vector search |
| Deployment | HuggingFace Spaces | Docker SDK |
| Python | 3.11+ | Async support |

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: RAG chat returns relevant textbook answers for 90%+ of topic-specific questions
- **SC-002**: Authentication flow (signup → signin → signout) works end-to-end
- **SC-003**: Personalization adapts content visibly based on experience level (beginner vs advanced)
- **SC-004**: Urdu translation produces readable Urdu text with preserved code blocks
- **SC-005**: All API endpoints respond within 60s (matching frontend timeout)
- **SC-006**: Backend deploys successfully on HuggingFace Spaces
- **SC-007**: Frontend on Vercel connects to HuggingFace backend without CORS errors
