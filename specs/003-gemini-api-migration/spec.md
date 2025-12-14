# Feature Specification: Gemini API Migration

**Feature Branch**: `003-gemini-api-migration`
**Created**: 2024-12-19
**Status**: Completed
**Input**: User request to migrate from OpenAI API to Google Gemini API for the RAG chatbot

## Clarifications

### Session 2024-12-19
- Q: Why migrate from OpenAI to Gemini? → A: OpenAI API key is not available; Gemini API key is available for the project.
- Q: What functionality needs to be preserved? → A: All existing functionality including chat, personalization, translation, and embeddings.
- Q: Should the frontend API interface change? → A: No, maintain the same API interface for frontend compatibility.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - RAG Chatbot with Gemini (Priority: P1)

As a student, I want to ask the AI Chat questions about the Physical AI textbook so that I can get contextually relevant answers using Gemini API.

**Why this priority**: Core functionality must work with the new API provider.

**Independent Test**: Send a POST request to `/api/chat` with a question and verify streaming response from Gemini.

**Acceptance Scenarios**:

1. **Given** the Gemini API is configured, **When** a user sends a POST request to `/api/chat` with a question, **Then** the system streams back a coherent answer using Gemini 1.5 Flash.
2. **Given** documents have been ingested with Gemini embeddings, **When** a user asks a question, **Then** the system retrieves relevant context from Qdrant and includes it in the response.
3. **Given** the system is running, **When** a user provides `selected_text`, **Then** the system prioritizes this text in the Gemini prompt.

---

### User Story 2 - Document Embeddings with Gemini (Priority: P1)

As a developer, I need the document ingestion to use Gemini's embedding model so that the vector database is compatible with the new API.

**Why this priority**: Embeddings must match between ingestion and query time.

**Independent Test**: Run ingestion and verify vectors are created using Gemini's text-embedding-004 model.

**Acceptance Scenarios**:

1. **Given** markdown files exist in the docs directory, **When** the ingestion process runs, **Then** embeddings are generated using Gemini's text-embedding-004 model.
2. **Given** embeddings are stored in Qdrant, **When** a chat query is made, **Then** the query embedding uses the same Gemini model for consistency.

---

### User Story 3 - Content Personalization with Gemini (Priority: P2)

As a student with a specific background, I want personalized content explanations so that I can learn more effectively.

**Why this priority**: Bonus feature for hackathon (50 points).

**Independent Test**: Send a POST request to `/api/personalize` with user background and verify personalized response.

**Acceptance Scenarios**:

1. **Given** a user has a software engineering background, **When** they request personalized content, **Then** Gemini generates explanations using software analogies.
2. **Given** a user has a mechanical engineering background, **When** they request personalized content, **Then** Gemini generates explanations using mechanical concepts.

---

### User Story 4 - Urdu Translation with Gemini (Priority: P2)

As an Urdu-speaking student, I want to translate textbook content to Urdu so that I can understand it better.

**Why this priority**: Bonus feature for hackathon (50 points).

**Independent Test**: Send a POST request to `/api/translate` with content and verify Urdu translation.

**Acceptance Scenarios**:

1. **Given** English textbook content, **When** a user requests Urdu translation, **Then** Gemini produces accurate Urdu translation preserving technical terms.

---

### Edge Cases

- What happens if GEMINI_API_KEY is missing? The system should fail gracefully on startup with a clear error message.
- How does the system handle Gemini API rate limits? Return appropriate error message to user.
- What if Gemini streaming fails mid-response? Append error message to stream and log the failure.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST use Google Gemini API (gemini-1.5-flash) for all chat completions instead of OpenAI GPT-4o.
- **FR-002**: The system MUST use Gemini's text-embedding-004 model for generating document embeddings.
- **FR-003**: The system MUST maintain the same external API interface (`/api/chat`, `/api/personalize`, `/api/translate`) for frontend compatibility.
- **FR-004**: The system MUST support streaming responses using Gemini's native streaming capability.
- **FR-005**: The system MUST configure the Gemini API key via the `GEMINI_API_KEY` environment variable.
- **FR-006**: The system MUST preserve all existing functionality including RAG retrieval, personalization, and translation.
- **FR-007**: The system MUST log all chat interactions to Neon Postgres database as before.

### Key Entities

- **GeminiTextbookAgent**: New agent class that handles chat interactions using Gemini API with streaming support.
- **EmbeddingService**: Updated service using Gemini's text-embedding-004 model.

## Out of Scope

- Changing the frontend API interface
- Adding new features beyond API migration
- Performance optimization beyond basic functionality
- Multi-model support (only Gemini)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Backend starts successfully with GEMINI_API_KEY configured.
- **SC-002**: Chat endpoint streams responses within 5 seconds of request.
- **SC-003**: Personalization endpoint returns personalized content based on user background.
- **SC-004**: Translation endpoint produces Urdu translations.
- **SC-005**: All chat interactions are logged to Neon Postgres database.
- **SC-006**: Document ingestion works with Gemini embeddings.
