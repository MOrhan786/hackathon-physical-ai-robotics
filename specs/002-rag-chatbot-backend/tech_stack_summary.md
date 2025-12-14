# Tech Stack Summary for RAG Chatbot Backend Implementation

This document compiles the key implementation details for the core technologies identified for the RAG Chatbot Backend, derived from Context7 documentation. This serves as a quick reference guide for the hackathon implementation.

---

## 1. FastAPI

**Purpose:** A modern, fast (high-performance) web framework for building APIs with Python 3.8+ based on standard Python type hints.

**Installation:**
```bash
pip install fastapi uvicorn
```

**Key Concepts / Core Usage:**
*   **App Instance:** `app = FastAPI()`
*   **Running the App:** `uvicorn main:app --reload` or `fastapi dev main.py` for development.
*   **Defining Endpoints:**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}
    ```
*   **Path Parameters:** `@app.get("/items/{item_id}")`
*   **Query Parameters:** `@app.get("/items/") def read_item(q: str | None = None)`
*   **Request Body (with Pydantic):**
    ```python
    from pydantic import BaseModel
    from fastapi import FastAPI

    class Item(BaseModel):
        name: str
        description: str | None = None

    @app.post("/items/")
    async def create_item(item: Item):
        return item
    ```
*   **Startup Events:** Use `@app.on_event("startup")` for initialization tasks (e.g., database connections, table creation in development).
*   **Dependency Injection:** Easily manage dependencies for endpoints.

**Integration Notes:**
*   Will form the core of the RAG Chatbot API, handling HTTP requests for chat and ingestion.
*   Leverages Pydantic for request and response data validation, ensuring type safety.

---

## 2. Uvicorn

**Purpose:** An ASGI (Asynchronous Server Gateway Interface) web server to run asynchronous Python web applications, like those built with FastAPI.

**Installation:** (Usually installed alongside FastAPI)
```bash
pip install uvicorn
```

**Key Concepts / Core Usage:**
*   **Command Line:** `uvicorn main:app` (where `main` is the Python file and `app` is the FastAPI instance).
*   **Reload Mode:** `uvicorn main:app --reload` for development, watching for code changes.
*   **Host and Port:** `uvicorn main:app --host 0.0.0.0 --port 8000`
*   **Workers:** `uvicorn main:app --workers 4` for production deployments.
*   **Programmatic Use:**
    ```python
    import uvicorn
    from main import app # Assuming your FastAPI app is named 'app' in main.py

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    ```

**Integration Notes:**
*   Essential for serving the FastAPI RAG Chatbot Backend application.
*   Will be configured for development (reload) and potentially for production (workers).

---

## 3. python-dotenv

**Purpose:** Reads key-value pairs from a `.env` file and sets them as environment variables, facilitating configuration management.

**Installation:**
```bash
pip install python-dotenv
```

**Key Concepts / Core Usage:**
*   **Basic Loading:**
    ```python
    from dotenv import load_dotenv
    load_dotenv() # Takes .env file in current dir by default
    import os
    api_key = os.getenv("API_KEY")
    ```
*   **Finding `.env`:** `from dotenv import find_dotenv; dotenv_path = find_dotenv()` can locate the file by searching parent directories.
*   **Custom Path:** `load_dotenv(dotenv_path="/path/to/.env")`
*   **Variable Expansion:** Supports referencing other variables within the `.env` file (e.g., `EMAIL=admin@${DOMAIN}`).

**Integration Notes:**
*   Will be used to load sensitive information and configuration (e.g., `OPENAI_API_KEY`, `QDRANT_URL`, `NEON_DB_URL`) from a `.env` file into the application's environment.
*   `backend/.env.example` will serve as a template.

---

## 4. Pydantic

**Purpose:** A data validation and settings management library for Python that uses type hints to define data schemas, ensuring data correctness and providing user-friendly errors.

**Installation:**
```bash
pip install pydantic
```

**Key Concepts / Core Usage:**
*   **Defining Models:**
    ```python
    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        name: str = "John Doe"
        email: str | None = None
    ```
*   **Validation:** Instances are validated upon creation.
    ```python
    user = User(id=1, name="Jane Doe", email="jane@example.com")
    # user = User(id="not_an_int") # This would raise a ValidationError
    ```
*   **JSON Schema Generation:** `User.model_json_schema()` generates an OpenAPI/JSON schema automatically, which FastAPI uses for its interactive documentation.
*   **Private Attributes:** Use `pydantic.PrivateAttr()` for internal attributes that should not be part of the schema or validation.

**Integration Notes:**
*   Crucial for defining the data models for API requests (e.g., chat message structure, ingestion payload) and responses.
*   Ensures strong typing and data integrity throughout the FastAPI application.

---

## 5. Qdrant-client

**Purpose:** A Python client library for interacting with the Qdrant vector search engine, used for storing, searching, and managing high-dimensional vectors.

**Installation:**
```bash
pip install qdrant-client
```

**Key Concepts / Core Usage:**
*   **Client Initialization (Sync):**
    ```python
    from qdrant_client import QdrantClient
    client = QdrantClient(host="localhost", port=6333) # Or QdrantClient(":memory:")
    ```
*   **Client Initialization (Async):**
    ```python
    from qdrant_client import AsyncQdrantClient
    async_client = AsyncQdrantClient(url="http://localhost:6333")
    ```
*   **Creating Collections:**
    ```python
    from qdrant_client import models
    client.create_collection(
        collection_name="my_collection",
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE) # size matches OpenAI embeddings
    )
    ```
*   **Adding Documents (with `fastembed` auto-embedding):**
    ```python
    documents = ["document one text", "document two text"]
    metadata = [{"source": "doc1"}, {"source": "doc2"}]
    ids = [1, 2]
    client.add(
        collection_name="my_collection",
        documents=documents,
        metadata=metadata,
        ids=ids
    )
    ```
*   **Querying:**
    ```python
    search_result = client.query(
        collection_name="my_collection",
        query_text="search query",
        limit=5
    )
    ```

**Integration Notes:**
*   Will be used by the `vector_store_service.py` to manage the Qdrant Cloud vector database.
*   Handles collection creation, upserting document embeddings (from markdown content), and retrieving relevant context for the LLM.

---

## 6. OpenAI Python Library

**Purpose:** Provides convenient access to the OpenAI REST API from Python applications for tasks like generating text completions, creating embeddings, and using the Assistants API.

**Installation:**
```bash
pip install openai
```

**Key Concepts / Core Usage:**
*   **Client Initialization:**
    ```python
    from openai import OpenAI
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
    ```
*   **Chat Completions (Streaming):**
    ```python
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
    ```
*   **Embeddings:**
    ```python
    response = client.embeddings.create(
        input=["Your text string goes here", "Another text string"],
        model="text-embedding-3-small"
    )
    embedding = response.data[0].embedding
    ```
*   **Assistants API (High-Level Abstraction for Agents):**
    *   Creating Assistants: `client.beta.assistants.create(...)`
    *   Creating Threads: `client.beta.threads.create(...)`
    *   Adding Messages: `client.beta.threads.messages.create(...)`
    *   Running the Assistant (with streaming): `client.beta.threads.runs.stream(...)` or `client.beta.threads.create_and_run_stream(...)`. This is relevant for "OpenAI Agents/ChatKit SDKs" mentions.

**Integration Notes:**
*   The `embedding_service.py` will use this to generate embeddings for document ingestion and user queries.
*   The `chat_service.py` will use this to interact with the LLM for generating responses, potentially leveraging streaming capabilities and the Assistants API.

---

## 7. beautifulsoup4

**Purpose:** A Python library for pulling data out of HTML and XML files, providing idiomatic ways to navigate, search, and modify the parse tree.

**Installation:**
```bash
pip install beautifulsoup4
```

**Key Concepts / Core Usage:**
*   **Parsing:**
    ```python
    from bs4 import BeautifulSoup
    html_doc = "<html><body><p>Hello, world!</p></body></html>"
    soup = BeautifulSoup(html_doc, 'html.parser') # 'lxml' is faster if installed
    ```
*   **Accessing Tags:** `soup.p`, `soup.title`
*   **Getting Text:** `soup.p.string` (for direct children), `soup.get_text()` (for all text)
*   **Finding Elements:**
    *   `soup.find('p', class_='intro')` (finds the first matching element)
    *   `soup.find_all('a')` (finds all `<a>` tags)
    *   Can search by tag name, attributes, string content, etc.
*   **Navigation:** `.parent`, `.next_sibling`, `.previous_sibling`, `.children`, `.descendants`

**Integration Notes:**
*   Will be used by the `document_loader.py` to parse markdown files (which often compile to HTML) to extract text content, especially when chunking by markdown headers, to prepare content for embedding.

---

## 8. psycopg2-binary

**Purpose:** A PostgreSQL database adapter for Python, providing a robust and efficient way to interact with PostgreSQL databases. The `-binary` version includes pre-compiled binaries, simplifying installation.

**Installation:**
```bash
pip install psycopg2-binary
```

**Key Concepts / Core Usage:**
*   **Connection:**
    ```python
    import psycopg2
    conn = psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    ```
*   **Cursor:** `cur = conn.cursor()`
*   **Executing Queries:** `cur.execute("SELECT * FROM users;")`
*   **Fetching Results:** `cur.fetchone()`, `cur.fetchmany(size)`, `cur.fetchall()`
*   **Committing/Rolling Back:** `conn.commit()`, `conn.rollback()`
*   **Closing:** `cur.close()`, `conn.close()`
*   **Parameterization (Security):** Always use parameterization for queries to prevent SQL injection.
    ```python
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", ("Alice", "alice@example.com"))
    ```

**Integration Notes:**
*   Will be used by the `db_service.py` to connect to the Neon Serverless Postgres database.
*   Handles logging chat interactions (user questions and AI responses) to the `chat_history` table.

---

## 9. Docusaurus

**Purpose:** A static-site generator that helps build and deploy modern documentation websites, leveraging React for interactive elements.

**Installation (CLI for new project):**
```bash
npx create-docusaurus@latest my-website classic
```

**Key Concepts / Core Usage:**
*   **Project Structure:** `docusaurus.config.js` (or `.ts`), `docs/`, `blog/`, `src/` (for React components), `static/`.
*   **Content:** Written in Markdown or MDX.
*   **Development Server:** `npm run start` or `npx docusaurus start` (usually at `http://localhost:3000`).
*   **Building:** `npm run build` (generates static HTML, CSS, JS).
*   **Deployment:** Static files can be deployed to GitHub Pages or other static hosting.
*   **React Components:** Custom components can be written in `src/components/` and used within Markdown/MDX.

**Integration Notes:**
*   The primary platform for the textbook itself.
*   The RAG Chatbot frontend (UI elements) will be embedded within the Docusaurus site.
*   The Docusaurus site will be deployed to GitHub Pages.

---

## 10. OpenAI Agents Python SDK

**Purpose:** A framework for building multi-agent workflows with LLMs, offering primitives like Agents, Handoffs, Guardrails, and Sessions, along with built-in tracing.

**Installation:**
```bash
pip install openai-agents
```

**Key Concepts / Core Usage:**
*   **Agent Definition:**
    ```python
    from agents import Agent, WebSearchTool, FileSearchTool

    agent = Agent(
        name="Assistant",
        tools=[WebSearchTool(), FileSearchTool(...)],
    )
    ```
*   **Running Agents:** Use `Runner.run(agent, "query", session=session)` to execute agent workflows.
*   **Realtime Runner:** `RealtimeRunner` for handling real-time interactions and event streaming.
*   **Sessions:** Support for different session types, including `EncryptedSession` and `SQLAlchemySession`, for managing conversation history and state.
*   **Tools:** Integrate various tools (e.g., `WebSearchTool`, `FileSearchTool`) to extend agent capabilities.

**Integration Notes:**
*   This SDK provides a higher-level abstraction for building the AI components of the RAG chatbot, especially for managing conversational flows and integrating different tools.
*   It can potentially be used in `chat_service.py` to orchestrate how the LLM interacts with the Qdrant vector store and other services.

---

## 11. ChatKit Python SDK

**Purpose:** Provides tools and functionalities for integrating ChatKit services and features into Python applications, focusing on building AI-powered chat experiences.

**Installation:**
```bash
pip install chatkit
```

**Key Concepts / Core Usage:**
*   **ChatKitServer:** `ChatKitServer(store=your_store, attachment_store=your_attachment_store)` to initialize the server, handling persistent data and optional file operations.
*   **Thread Items:** `ThreadItem` represents individual messages or events in a conversation.
*   **User Message Items:** `UserMessageItem` for user-generated messages, including content, attachments, and inference options.
*   **Actions:** `ActionConfig` can be attached to UI elements (e.g., buttons) to trigger server-side actions, such as updating widgets or running inference.
*   **Widget Definitions:** Supports defining UI widgets (e.g., `Button`, `Text`, `Image`) with properties like `Justification`, `Alignment`, `TextAlign`.

**Integration Notes:**
*   This SDK seems geared towards building the *backend* for a rich chat UI, handling the server-side logic for chat interactions.
*   It could be used in conjunction with FastAPI to expose endpoints that interact with the ChatKit server, managing conversational state and UI elements.
*   Might be relevant for how the RAG chatbot frontend (embedded in Docusaurus) communicates with the FastAPI backend, especially if a rich, interactive chat UI is planned.

---