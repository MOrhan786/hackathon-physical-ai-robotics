# Quickstart: RAG Chatbot Backend

This guide explains how to set up and run the RAG Chatbot Backend locally.

## 1. Prerequisites

-   Python 3.12+
-   `pip` and `uv` for package installation and running the server.
-   Access to OpenAI, Qdrant, and Neon accounts.

## 2. Setup

### a. Environment Variables

Create a `.env` file in the `backend/` directory. You can copy the `.env.example` file:

```bash
cp .env.example .env
```

Now, fill in the values in the `.env` file:

```
OPENAI_API_KEY="sk-..."
QDRANT_URL="https://..."
QDRANT_API_KEY="..."
NEON_DB_URL="postgres://..."
API_KEY="a-secure-random-string" # Pre-shared key for API access
```

### b. Install Dependencies

It is recommended to use a virtual environment.

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## 3. Running the Application

### a. Start the Server

Use `uvicorn` to run the FastAPI application:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### b. Run Ingestion

To populate the vector database, send a POST request to the `/ingest` endpoint:

```bash
curl -X POST http://localhost:8000/ingest \
-H "X-API-Key: your-api-key"
```

This will read the markdown files from the `docs/` directory, create embeddings, and upsert them into your Qdrant collection.

### c. Test the Chat

Send a POST request to the `/api/chat` endpoint:

```bash
curl -X POST http://localhost:8000/api/chat \
-H "Content-Type: application/json" \
-H "X-API-Key: your-api-key" \
-d 
'{
  "message": "What is Physical AI?"
}'
```
