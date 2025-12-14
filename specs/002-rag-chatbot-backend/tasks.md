# Tasks: RAG Chatbot Backend

This document outlines the development tasks for the RAG Chatbot Backend feature. Each task is designed to be independently executable and testable where possible.

**Feature**: `002-rag-chatbot-backend`
**Spec**: [`specs/002-rag-chatbot-backend/spec.md`](./spec.md)
**Plan**: [`specs/002-rag-chatbot-backend/plan.md`](./plan.md)

## Implementation Strategy

The implementation will proceed in phases, prioritizing the core functionality (chat) by first establishing the necessary data ingestion pipeline.

1.  **Phase 1 & 2 (Setup & Foundational)**: Initialize the project structure and configure core services.
2.  **Phase 3 (User Story 2)**: Implement the document ingestion feature.
3.  **Phase 4 (User Story 1)**: Implement the chat functionality.
4.  **Phase 5 (User Story 3)**: Implement chat history logging.
5.  **Phase 6 (Polish)**: Add final polish and handle cross-cutting concerns.

## Phase 1: Setup

- [X] T001 Create the `backend/` directory for the FastAPI application.
- [X] T002 Create the project structure inside `backend/` as defined in `plan.md`: `src/main.py`, `src/api/`, `src/core/`, `src/models/`, `src/services/`.
- [X] T003 Create `backend/requirements.txt` with initial dependencies: `fastapi`, `uvicorn`, `python-dotenv`, `pydantic`.
- [X] T004 Create `backend/.env.example` with placeholders for `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`, `NEON_DB_URL`, and `API_KEY`.
- [X] T005 Create a basic FastAPI app instance in `backend/src/main.py`.

## Phase 2: Foundational Services

- [X] T006 [P] Implement configuration loading in `backend/src/core/config.py` to read environment variables from the `.env` file.
- [X] T007 [P] Implement the API Key security dependency in a new file `backend/src/api/security.py`.

## Phase 3: User Story 2 - Documentation Ingestion (P2)

**Goal**: As a developer, I need a way to process markdown files, create embeddings, and store them in a Qdrant vector database.
**Independent Test**: The Qdrant collection for the textbook contains vector embeddings corresponding to the content of the markdown files after the process is run.

- [X] T008 [US2] Add `qdrant-client`, `openai` (for embeddings and chat completions), and `beautifulsoup4` to `backend/requirements.txt`.
- [X] T009 [US2] Implement a document loader in a new file `backend/src/services/document_loader.py` to read and parse `.md` files from the `physical-ai-textbook/docs/` directory.
- [X] T010 [US2] Implement text chunking logic in `backend/src/services/document_loader.py` to split documents by markdown headers.
- [X] T011 [US2] Implement the embedding service in `backend/src/services/embedding_service.py` to generate embeddings using OpenAI's `text-embedding-3-small` model.
- [X] T012 [US2] Implement the vector store service in `backend/src/services/vector_store_service.py` to handle interactions with Qdrant, including collection creation and upserting vectors.
- [X] T013 [US2] Create the `/ingest` endpoint in a new file `backend/src/api/ingest.py` that uses the document loader, embedding service, and vector store service to perform the ingestion process.
- [X] T014 [US2] Add the ingest router to `backend/src/main.py`.

## Phase 4: User Story 1 - Student Gets Textbook Answers (P1)

**Goal**: As a student, I want to ask the AI Chat a question about the course material so that I can get immediate, contextually relevant answers.
**Independent Test**: A `POST` request to `/api/chat` with a question yields a factually correct and relevant streamed response.

- [X] T015 [US1] Define the `ChatRequest` Pydantic model in `backend/src/models/chat.py`.
- [X] T016 [US1] Implement the core chat logic in `backend/src/services/chat_service.py`. This service will:
    - Take a user message.
    - Create a vector from the message using `embedding_service`.
    - Search for relevant context chunks from Qdrant using `vector_store_service`.
    - Construct a prompt for the OpenAI API with the user message and context.
    - Call the OpenAI API using "OpenAI Agents/ChatKit SDKs" to get a streaming response.
- [X] T017 [US1] Create the `/api/chat` endpoint in a new file `backend/src/api/chat.py` that uses the `chat_service` to handle chat requests and return a `StreamingResponse`.
- [X] T018 [US1] Add the chat router to `backend/src/main.py`.
- [X] T019 [US1] Implement the "no documents found" disclaimer logic in `backend/src/services/chat_service.py` as per the spec.
- [X] T020 [US1] Implement logic in `backend/src/services/chat_service.py` to prioritize `selected_text` as additional context for the LLM prompt (FR-014).

## Phase 5: User Story 3 - Administrator Logs Chat History (P3)

**Goal**: As an administrator, I need every user interaction with the chatbot to be logged in a persistent database.
**Independent Test**: An interaction with `/api/chat` results in a new, correct record in the Neon Postgres `chat_history` table.

- [X] T021 [US3] Add `psycopg2-binary` to `backend/requirements.txt`.
- [X] T022 [US3] Implement a database service in a new file `backend/src/services/db_service.py` to handle the connection to the Neon Postgres database.
- [X] T023 [US3] Create a function in `db_service.py` to log a chat interaction to the `chat_history` table.
- [X] T024 [US3] Integrate the logging function into the `chat_service` to save the user message and the full AI response after the stream is complete.

## Phase 6: Polish & Cross-cutting Concerns

- [X] T025 Create `tests/` directory with `integration/` and `unit/` subdirectories.
- [X] T026 [P] Implement graceful failure handling for missing environment variables in `backend/src/core/config.py`.
- [X] T027 [P] Add input validation to the `/api/chat` endpoint to handle malformed requests.
- [X] T028 [P] Implement error handling for OpenAI Agents/ChatKit SDKs failures during streaming in `backend/src/services/chat_service.py`.
- [X] T029 Create `README.md` for the backend service with setup and execution instructions.
- [X] T030 [P] Enforce Python quality standards: type hints and Google-style docstrings in `backend/src/`.
- [X] T031 Create Architectural Decision Record (ADR) for RAG retrieval logic in `history/adr/`.
- [X] T032 [P] Implement performance benchmarks for ingestion (SC-001) in `tests/integration/test_performance.py`.
- [X] T033 [P] Implement performance tests for chat response time (SC-002) in `tests/integration/test_performance.py`.

## Dependencies

- **US1 depends on US2**: The chat functionality cannot work without the ingestion pipeline being in place.
- **US3 depends on US1**: Logging requires a chat interaction to have occurred.

## Parallel Execution

- Within each phase, tasks marked with `[P]` can often be worked on in parallel.
- **Phase 2** tasks are independent and can be done concurrently.
- In **Phase 3**, `T008` to `T012` can be developed in parallel to some extent, but they all need to come together for `T013`.
- In **Phase 4**, `T015` and `T016` can be started, but `T017` depends on them.
- **Phase 6** tasks are largely independent and can be picked up in parallel.
