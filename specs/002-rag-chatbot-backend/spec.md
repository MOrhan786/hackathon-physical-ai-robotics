# Feature Specification: RAG Chatbot Backend & Ingestion Engine

**Feature Branch**: `002-rag-chatbot-backend`
**Created**: 2025-11-29
**Status**: Draft
**Input**: User description: "I need a technical specification for the Python Backend API that powers the 'AI Chat' feature."

## Clarifications

### Session 2025-11-29
- Q: What is the required security mechanism for the `/api/chat` and `/ingest` endpoints? → A: The backend requires a pre-shared secret key to be present in an HTTP header (e.g., `X-API-Key`) for all requests.
- Q: What should the chatbot do if the vector search returns no relevant documents for a user's question? → A: The LLM should answer from its knowledge, but it should also state that this information was from its own knowledge rather than the accurate vector database.
- Q: What is the desired behavior if the connection to the OpenAI API fails mid-stream? → A: The system attempts to send a structured error message to the user (e.g., appended to the stream) indicating a server-side problem.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Gets Textbook Answers (Priority: P1)

As a student, I want to ask the AI Chat a question about the course material so that I can get immediate, contextually relevant answers based on the official textbook.

**Why this priority**: This is the core value proposition for the end-user. The chat feature is only useful if it can accurately answer student questions based on the provided content.

**Independent Test**: Can be tested by sending a `POST` request to the `/api/chat` endpoint with a question related to the ingested 'Module 1' content and verifying the streamed response is accurate and relevant.

**Acceptance Scenarios**:

1.  **Given** the documentation for "Module 1" has been ingested, **When** a user sends a POST request to `/api/chat` with the message "What is Physical AI?", **Then** the system streams back a coherent answer that is factually based on the content of Module 1.
2.  **Given** the system is running, **When** a user asks a question unrelated to the ingested content, **Then** the system provides a response indicating it may not have the answer (e.g., "I can only answer questions based on the provided textbook material.").
3.  **Given** the documentation for "Module 1" has been ingested, **When** a user sends a POST request to `/api/chat` with a general question and relevant text selected from "Module 1", **Then** the system streams back a coherent answer that is factually based on the provided selected text and the original "Module 1" content.

---

### User Story 2 - Developer Ingests Documentation (Priority: P2)

As a developer, I need a way to process all the markdown files from the `docs/` directory, create embeddings, and store them in the Qdrant vector database, so that the chatbot has the necessary knowledge base to answer questions.

**Why this priority**: This is a foundational requirement. The chat feature cannot function without the content ingestion pipeline being in place and working correctly.

**Independent Test**: Can be tested by running the ingestion script/endpoint and then querying the Qdrant vector database directly to confirm that vectors for the documents now exist.

**Acceptance Scenarios**:

1.  **Given** a `docs/` directory containing several `.md` files, **When** the ingestion process is triggered (e.g., via the `/ingest` endpoint), **Then** the Qdrant collection for the textbook contains new vector embeddings corresponding to the content of the markdown files.
2.  **Given** the ingestion process has been run once, **When** it is run a second time, **Then** the vector database is updated with the latest content without creating duplicate entries for unchanged text.

---

### User Story 3 - Administrator Logs Chat History (Priority: P3)

As an administrator or teaching assistant, I need every user interaction with the chatbot to be logged in a persistent database (Neon Postgres) so that we can review chat history for quality control, audit, and analysis purposes.

**Why this priority**: This is a stated requirement for the project ("Hackathon requirement") and is essential for monitoring the feature's usage and performance.

**Independent Test**: Can be tested by sending a request to `/api/chat`, and then querying the Neon Postgres database to verify that a new record corresponding to that interaction has been created.

**Acceptance Scenarios**:

1.  **Given** a user has just received a response from the chatbot, **When** an administrator queries the `chat_history` table in the Neon Postgres database, **Then** a new row exists containing the user's message, the AI's response, and a timestamp.

---

### Edge Cases

-   What happens if the `.env` file is missing or a required API key is invalid? The system should fail gracefully on startup with a clear error message.
-   How does the system handle an empty `docs/` directory during ingestion? It should complete without errors and the vector database should remain empty.
-   What is the behavior if a user submits a very long or malformed message to the `/api/chat` endpoint? The API should return a validation error.
-   How should the system handle a failure while streaming a response from the OpenAI API? It should attempt to append a structured error message to the stream to inform the user of the failure.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide an ingestion mechanism (e.g., a script or an API endpoint) that reads all `.md` files from the `docs/` directory.
-   **FR-002**: During ingestion, the system MUST chunk the text from the markdown files by splitting the content based on section headers (e.g., ##, ###).
-   **FR-003**: The system MUST generate vector embeddings for each text chunk using the OpenAI `text-embedding-3-small` model.
-   **FR-004**: The system MUST upsert the generated vectors into a Qdrant vector database.
-   **FR-005**: The system MUST expose a `POST /api/chat` endpoint that accepts a JSON payload containing `{ message: string, history: list, selected_text: string | null }`.
-   **FR-006**: The `/api/chat` endpoint logic MUST convert the incoming user message to a vector and search the Qdrant database for the top 3 most relevant text chunks.
-   **FR-007**: The system MUST construct a detailed prompt for the language model, including the retrieved context chunks and the user's message, prefixed with the persona "You are a Professor."
-   **FR-008**: The system MUST stream the response from the language model back to the client.
-   **FR-009**: The system MUST log every complete chat interaction (user message and full AI response) to a Neon Serverless Postgres database.
-   **FR-010**: The database schema for chat history MUST include at a minimum: a unique `id`, `user_message`, `ai_response`, and a `timestamp`.
-   **FR-011**: All external service credentials and security keys (e.g., OPENAI_API_KEY, QDRANT_URL, NEON_DB_URL, API_KEY) MUST be configurable via environment variables (e.g., from a `.env` file).
-   **FR-012**: The system MUST protect all API endpoints by validating a static, pre-shared API key sent in an HTTP header.
-   **FR-013**: If the vector database search yields no relevant document chunks, the system MUST forward the user's question to the LLM without context and prepend the response with a disclaimer, such as "As I could not find a relevant answer in the provided textbook, this answer is based on my general knowledge:".
-   **FR-014**: If `selected_text` is provided in the `POST /api/chat` request, the system MUST prioritize this text as additional context for the LLM prompt.

### Key Entities

-   **Document Chunk**: A segment of text extracted from a source markdown file. It has content (the text itself) and metadata (like its source file). This is the unit of information stored in the vector database.
-   **Chat Interaction**: A record of a single turn in a conversation, containing the user's message, the AI's full response, and a timestamp. This is the unit of information stored in the Postgres logging database.

## Out of Scope

-   Complex user-level authentication and authorization (the API is protected by a single, static API key).
-   A user interface for viewing or managing chat history from the database.
-   Real-time or automated (e.g., webhook-based) ingestion triggers. The ingestion process is assumed to be manually initiated.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: The ingestion process can successfully process 100 markdown files, averaging 5 pages each, in under 5 minutes.
-   **SC-002**: The `/api/chat` endpoint begins streaming a response to the user in under 3 seconds for 95% of requests.
-   **SC-003**: When asked 10 different questions drawn directly from the "Module 1" content, the chatbot provides an answer that scores 4 or higher on a 5-point rubric (1: Incorrect, 5: Fully Correct and Relevant) for at least 8 of them. (Rubric to be defined in test plan)
-   **SC-004**: 100% of chat interactions via the `/api/chat` endpoint result in a corresponding record being created in the Neon Postgres database.
