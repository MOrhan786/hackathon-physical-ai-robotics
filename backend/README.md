---
title: Physical AI Textbook API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Physical AI & Humanoid Robotics Textbook - Backend API

FastAPI backend with RAG chatbot, authentication, content personalization, and Urdu translation.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/chat` | RAG-based chat with textbook content |
| POST | `/api/auth/signup` | User registration with background profiling |
| POST | `/api/auth/signin` | User login |
| POST | `/api/auth/signout` | User logout |
| POST | `/api/personalize` | Content personalization based on user level |
| POST | `/api/translate` | Content translation (default: Urdu) |

## Tech Stack

- **Framework**: FastAPI
- **Vector DB**: Qdrant Cloud
- **Auth DB**: PostgreSQL (Neon)
- **LLM**: OpenAI GPT-4o-mini
- **Embeddings**: OpenAI text-embedding-3-small

## Setup

1. Copy `.env.example` to `.env` and fill in credentials
2. Install dependencies: `pip install -r requirements.txt`
3. Run ingestion: `python ingest.py`
4. Start server: `python main.py`
