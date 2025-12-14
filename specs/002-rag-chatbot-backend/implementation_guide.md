# Implementation Guide: RAG Chatbot Backend

This document consolidates detailed implementation guidance for the RAG Chatbot Backend, drawing from web searches and project specifications. It serves as a living reference for leveraging the specified tech stack (Python, FastAPI, OpenAI, Qdrant, Neon Postgres).

## Table of Contents

1.  [FastAPI Integration](#1-fastapi-integration)
2.  [Uvicorn Usage](#2-uvicorn-usage)
3.  [Configuration with `python-dotenv` & `pydantic-settings`](#3-configuration-with-python-dotenv--pydantic-settings)
4.  [OpenAI Python Library](#4-openai-python-library)
    *   [Embeddings](#embeddings)
    *   [Chat Completions (Agents/ChatKit SDKs)](#chat-completions-agentschatkit-sdks)
5.  [Qdrant Client (`qdrant-client`)](#5-qdrant-client-qdrant-client)
6.  [PostgreSQL Integration with `asyncpg` & `SQLAlchemy[asyncio]`](#6-postgresql-integration-with-asyncpg--sqlalchemyasyncio)
7.  [PDF Text Extraction (`pypdf`)](#7-pdf-text-extraction-pypdf)
8.  [Word Document Text Extraction (`python-docx`)](#8-word-document-text-extraction-python-docx)
9.  [Token Counting (`tiktoken`)](#9-token-counting-tiktoken)
10. [Document Chunking (`langchain-text-splitters`)](#10-document-chunking-langchain-text-splitters)

---

## 1. FastAPI Integration

**Purpose**: Build the web API endpoints for the RAG chatbot.
**Key Takeaways**:
*   Define API endpoints (e.g., `/chat`, `/ingest`) using FastAPI decorators.
*   Utilize Pydantic models for request body validation and response serialization.
*   Implement `startup` and `shutdown` events for resource management (e.g., database connection pools).
*   Structure the application with routers and services for modularity.

**Example `main.py` structure (conceptual):**

```python
# rag_chatbot/main.py
from fastapi import FastAPI
from app.api import chat, document_ingestion
from app.core.config import settings
from app.core.db import database # Assuming a global database object/function

app = FastAPI(
    title=settings.app_name,
    description="FastAPI service for a RAG-enabled chatbot.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    # Initialize database connections, Qdrant client, OpenAI client, etc.
    await database.connect() # Example
    print("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    # Close database connections, release resources.
    await database.disconnect() # Example
    print("Application shutdown complete.")

# Include API routers
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(document_ingestion.router, prefix="/api/ingest", tags=["Ingestion"])

@app.get("/")
async def root():
    return {"message": "RAG Chatbot Backend is running."}

# To run with Uvicorn:
# uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 2. Uvicorn Usage

**Purpose**: Serve the FastAPI application.
**Key Takeaways**:
*   Uvicorn is the ASGI server that runs the FastAPI application.
*   **Command**: `uvicorn <module_name>:<fastapi_app_instance> [options]`
*   **Typical usage for development**: `uvicorn rag_chatbot.main:app --host 0.0.0.0 --port 8000 --reload --log-level info`
    *   `rag_chatbot.main`: Refers to the `main.py` file within the `rag_chatbot` package.
    *   `app`: Refers to the `FastAPI` application instance named `app` inside `main.py`.
    *   `--reload`: Enables auto-reloading during development.

## 3. Configuration with `python-dotenv` & `pydantic-settings`

**Purpose**: Manage application settings from environment variables and `.env` files.
**Key Takeaways**:
*   `pydantic-settings.BaseSettings` automatically loads configurations.
*   Define a `Settings` class inheriting `BaseSettings` with type hints and optional defaults.
*   `SettingsConfigDict` is used to specify `.env` file location, encoding, and other behaviors.
*   Example configuration in `app/core/config.py` is robust.

**Example `app/core/config.py`:**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str
    neon_database_url: str
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str = ""
    app_name: str = "RAG Chatbot Backend" # Example additional setting

settings = Settings()
```

## 4. OpenAI Python Library

**Purpose**: Generate embeddings and interact with LLMs for chat completions.
**Key Takeaways**:
*   The `openai` Python library (with `AsyncOpenAI`) is the core tool.
*   "OpenAI Agents/ChatKit SDKs" is a conceptual framework built on this library, involving prompt strategies and service orchestration, not a separate installation.

### Embeddings

*   **Model**: `text-embedding-3-small` (as per `spec.md`).
*   **Usage**: Initialize an OpenAI client (e.g., `AsyncOpenAI`) and use `client.embeddings.create()` to convert text into vector representations.

### Chat Completions (Agents/ChatKit SDKs)

*   **Usage**: The `ChatService` will orchestrate LLM calls using `client.chat.completions.create()`.
*   **Features**: Supports streaming responses, prompt strategies (`BasePromptStrategy`, `RoleBasedStrategy`, `KnowledgeEnhancedStrategy`), and context management.
*   **Dependencies**: Ensure `openai` is in `requirements.txt`.

## 5. Qdrant Client (`qdrant-client`)

**Purpose**: Store and retrieve vector embeddings.
**Key Takeaways**:
*   **Installation**: `pip install qdrant-client`.
*   **Client Initialization**: `QdrantClient(host=..., port=..., api_key=...)`.
*   **Collection Creation**: `client.recreate_collection()` or `client.create_collection()` with `models.VectorParams(size=EMBEDDING_DIM, distance=models.Distance.COSINE)`.
*   **Data Ingestion**:
    1.  Generate embeddings for document chunks.
    2.  Create `models.PointStruct` objects (id, vector, payload).
    3.  Upload with `client.upsert()`.
*   **Retrieval**:
    1.  Embed the user query.
    2.  Use `client.search()` with the query vector and `limit` to find top-k relevant chunks.
    3.  Retrieve original text from `hit.payload`.

## 6. PostgreSQL Integration with `asyncpg` & `SQLAlchemy[asyncio]`

**Purpose**: Store document metadata, chat sessions, and messages in Neon Postgres asynchronously.
**Key Takeaways**:
*   **Driver**: Use `asyncpg` as the asynchronous driver for PostgreSQL. `psycopg2-binary` is **not** recommended for async operations.
*   **Installation**: `pip install "SQLAlchemy[asyncio]" asyncpg`.
*   **Connection String**: Use `postgresql+asyncpg://...`.
*   **SQLAlchemy Setup**:
    *   `create_async_engine(DATABASE_URL)`.
    *   `sessionmaker` with `AsyncSession`.
    *   Use `AsyncSessionLocal` context manager for DML/query operations.
    *   `await conn.run_sync(Base.metadata.create_all)` for schema creation within an async context.
*   **Connection Management**: Use FastAPI's `lifespan` events to create (`create_pool`) and close (`pool.close()`) an `asyncpg` connection pool.
*   **Dependency Injection**: Provide database connections from the pool to FastAPI routes using `Depends`.

## 7. PDF Text Extraction (`pypdf`)

**Purpose**: Extract textual content from PDF documents for ingestion.
**Key Takeaways**:
*   **Installation**: `pip install pypdf`.
*   **Functions**:
    *   `extract_text_from_pdf_path(pdf_path: str)`: For local PDF files.
    *   `extract_text_from_pdf_bytes(pdf_bytes: bytes)`: For PDF content received as bytes (e.g., from network upload).
*   **Process**: Open PDF, iterate pages with `PdfReader`, and use `page.extract_text()`.
*   **Error Handling**: Implement `try-except` blocks for `FileNotFoundError`, `PdfReadError`, etc.

## 8. Word Document Text Extraction (`python-docx`)

**Purpose**: Extract textual content from Word (`.docx`) documents for ingestion.
**Key Takeaways**:
*   **Installation**: `pip install python-docx`.
*   **Function**:
    *   `extract_text_from_docx(docx_path: str)`: Opens a `.docx` file and iterates through `document.paragraphs` to collect text.
*   **Process**: Load document with `docx.Document()`, then loop through `document.paragraphs`.

## 9. Token Counting (`tiktoken`)

**Purpose**: Manage context window, estimate costs, and optimize prompt engineering.
**Key Takeaways**:
*   **Installation**: `pip install tiktoken`.
*   **Usage**: `tiktoken.encoding_for_model(model_name)` to get the tokenizer, then `encoding.encode(text)` to get tokens.
*   **Function**: `count_tokens(text: str, model_name: str) -> int`.
*   **Integration**: Use during prompt construction to ensure LLM context window limits are not exceeded and to inform chunking strategies.

## 10. Document Chunking (`langchain-text-splitters`)

**Purpose**: Break down large documents into smaller, semantically meaningful chunks.
**Key Takeaways**:
*   **Installation**: `pip install langchain-text-splitters`.
*   **Primary Tool**: `RecursiveCharacterTextSplitter` is highly flexible.
*   **Configuration**: `chunk_size`, `chunk_overlap`, and a list of `separators`.
*   **Process**:
    1.  Load raw document text.
    2.  Instantiate `RecursiveCharacterTextSplitter` with desired parameters.
    3.  Call `splitter.split_text(content)`.
*   **Integration**: These chunks are then embedded and stored in Qdrant. Critical for efficient RAG retrieval.
*   **Other Splitters**: Be aware of `TokenTextSplitter` (token-based) and sentence-based splitters for specific needs.

---
This guide forms the technical blueprint for the `002-rag-chatbot-backend` implementation.
