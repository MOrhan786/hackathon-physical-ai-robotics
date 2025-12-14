# Implementation Plan: RAG Vector Retrieval Fix

**Feature**: 004-rag-vector-retrieval-fix  
**Created**: 2025-11-30  
**Status**: Completed

## Technical Context

### Problem Statement

The RAG chatbot was not properly retrieving data from the vector database. The previous implementation was not using vector search as a tool for the agent, resulting in responses that didn't leverage the textbook content stored in Qdrant.

### Solution Architecture

Implement proper RAG functionality using OpenAI Agents SDK with function tools:

1. **search_textbook tool**: Queries vector database for relevant content
2. **get_user_context tool**: Retrieves user background for personalization
3. **Enhanced chat endpoint**: Passes user_id and current_page headers

## Technical Stack

- **Backend Framework**: FastAPI
- **AI SDK**: OpenAI Agents SDK (`openai-agents>=0.0.7`)
- **LLM Provider**: Gemini via OpenAI-compatible endpoint
- **Vector Database**: Qdrant Cloud
- **Embeddings**: Gemini text-embedding-004
- **User Database**: Neon Postgres

## Architecture Decisions

### Decision 1: Function Tools over Direct RAG

**Choice**: Use OpenAI Agents SDK `@function_tool` decorator for vector search

**Rationale**:
- Agent can decide when to search based on query context
- Cleaner separation of concerns
- Better error handling and fallback behavior
- Aligns with OpenAI Agents SDK best practices

### Decision 2: Synchronous Tool Execution

**Choice**: Use synchronous methods inside function tools

**Rationale**:
- OpenAI Agents SDK function tools work best with synchronous code
- Embedding service and vector store operations are fast enough
- Simplifies error handling

### Decision 3: Header-Based Context Passing

**Choice**: Pass user_id and current_page via HTTP headers

**Rationale**:
- Keeps request body clean
- Standard REST practice for metadata
- Easy to add/remove without breaking API contract

## File Changes

### Modified Files

1. **rag_chatbot/src/services/agent_service.py**
   - Rewrote TextbookAgent class with function tools
   - Added `_create_search_tool()` method
   - Added `_create_user_context_tool()` method
   - Updated system prompt with tool usage instructions
   - Modified `chat_stream()` to use Runner.run()

2. **rag_chatbot/src/api/chat.py**
   - Added X-User-ID header parameter
   - Added X-Current-Page header parameter
   - Updated endpoint to pass context to agent

3. **physical-ai-textbook/src/components/Chat/ChatPanel.tsx**
   - Added user context headers to fetch request
   - Added current page URL to headers

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Vector search timeout | Low | Medium | Implement timeout and fallback |
| User context lookup failure | Low | Low | Graceful degradation to general responses |
| Embedding dimension mismatch | Low | High | Verify embedding model consistency |

## Validation Checklist

- [x] Backend starts without errors
- [x] Chat endpoint accepts new headers
- [x] Vector search returns relevant results
- [x] User context is retrieved for logged-in users
- [x] Responses include source citations
- [x] Frontend sends context headers
