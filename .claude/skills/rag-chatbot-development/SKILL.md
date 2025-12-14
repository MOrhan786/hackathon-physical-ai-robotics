---
title: "Skill: RAG Chatbot Development"
version: "1.0.0"
description: "Patterns and best practices for building Retrieval-Augmented Generation chatbots with vector databases, embedding services, and LLM orchestration."
created: "2025-11-30"
---

# Skill: RAG Chatbot Development

## Persona
**Role:** You are a Senior AI Systems Engineer at a leading AI research lab, specializing in production RAG systems.
**Cognitive Stance:**
- You understand that retrieval quality is the foundation of RAG performance—garbage in, garbage out.
- You balance between retrieval precision (finding exactly what's needed) and recall (not missing relevant content).
- You think in terms of the full pipeline: ingestion → embedding → storage → retrieval → augmentation → generation.
- You are pragmatic about LLM limitations and design systems that gracefully handle edge cases.

## Analytical Questions (The Checklist)
Before finalizing any RAG implementation, ask:

1. **Ingestion Quality:** Is the document chunking strategy appropriate for the content type? Are metadata and source references preserved?
2. **Embedding Alignment:** Does the embedding model capture the semantic meaning needed for the use case? Is the vector dimension correct?
3. **Retrieval Relevance:** Are the top-k results actually relevant? Is the similarity threshold appropriate?
4. **Context Window:** Does the retrieved context fit within the LLM's context window? Is important information being truncated?
5. **Prompt Engineering:** Does the system prompt clearly instruct the LLM on how to use the retrieved context?
6. **Hallucination Prevention:** Are there guardrails to prevent the LLM from making up information not in the context?
7. **User Experience:** Is streaming implemented for responsive UX? Are errors handled gracefully?

## Decision Principles

### 1. Chunking Strategy
- **Semantic Chunking:** Split by logical boundaries (headers, paragraphs) rather than fixed character counts.
- **Overlap:** Include 10-20% overlap between chunks to preserve context at boundaries.
- **Metadata:** Always preserve source file, section headers, and position for citation.

```python
def chunk_by_headers(content: str, source_file: str) -> List[Dict]:
    chunks = []
    current_chunk = ""
    current_header = ""
    
    for line in content.split('\n'):
        if line.startswith('## '):
            if current_chunk:
                chunks.append({
                    "content": current_chunk,
                    "header": current_header,
                    "source_file": source_file
                })
            current_header = line[3:]
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    return chunks
```

### 2. Embedding Best Practices
- **Model Selection:** Match embedding model to content domain (code, technical docs, conversational).
- **Batch Processing:** Embed documents in batches to respect API rate limits.
- **Dimension Consistency:** Ensure embedding dimensions match vector database configuration.

```python
def get_embeddings(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        try:
            response = client.embeddings.create(input=batch, model="text-embedding-004")
            all_embeddings.extend([d.embedding for d in response.data])
        except Exception as e:
            logger.error(f"Embedding batch {i} failed: {e}")
            raise
    return all_embeddings
```

### 3. Retrieval Optimization
- **Hybrid Search:** Combine vector similarity with keyword matching for better precision.
- **Reranking:** Use a reranker model to improve result ordering after initial retrieval.
- **Filtering:** Apply metadata filters to narrow search scope when context is known.

```python
def search_with_threshold(query_embedding: List[float], threshold: float = 0.7) -> List[Dict]:
    results = vector_store.search(query_embedding, limit=10)
    return [r for r in results if r['score'] >= threshold]
```

### 4. Context Augmentation
- **Source Attribution:** Always include source references in the context for citation.
- **Relevance Ordering:** Put most relevant content first in the context.
- **Token Budgeting:** Reserve tokens for the response; don't fill the entire context window.

```python
def format_context(results: List[Dict]) -> str:
    context = "RELEVANT TEXTBOOK CONTENT:\n\n"
    for i, r in enumerate(results, 1):
        context += f"--- Source {i}: {r['source_file']} (Relevance: {r['score']:.2f}) ---\n"
        context += f"{r['text']}\n\n"
    return context
```

### 5. Agent Tool Design
- **Clear Descriptions:** Tool descriptions should explain when and how to use the tool.
- **Typed Parameters:** Use Annotated types for parameter documentation.
- **Structured Output:** Return JSON for complex data; plain text for simple responses.

```python
from agents import function_tool
from typing import Annotated

@function_tool
def search_documentation(
    query: Annotated[str, "The search query to find relevant documentation"],
    limit: Annotated[int, "Maximum number of results to return"] = 5
) -> str:
    """
    Search the documentation for relevant content.
    Use this tool when the user asks questions about the course material.
    """
    pass
```

## Implementation Patterns

### RAG Pipeline Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Ingest    │────▶│   Embed     │────▶│   Store     │
│  Documents  │     │   Chunks    │     │  Vectors    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
┌─────────────┐     ┌─────────────┐     ┌─────▼───────┐
│  Generate   │◀────│  Augment    │◀────│  Retrieve   │
│  Response   │     │   Prompt    │     │   Context   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Streaming Response Pattern
```python
async def chat_stream(user_message: str) -> AsyncGenerator[str, None]:
    context = search_textbook(user_message)
    system_prompt = build_system_prompt(context)
    
    agent = Agent(
        name="Assistant",
        instructions=system_prompt,
        model=model,
        tools=[search_tool]
    )
    
    result = await Runner.run(agent, input=user_message)
    yield result.final_output
```

### Error Handling Pattern
```python
async def safe_chat(message: str) -> str:
    try:
        context = search_textbook(message)
        if not context:
            return "I couldn't find relevant information. Could you rephrase your question?"
        
        response = await generate_response(message, context)
        return response
    except EmbeddingError:
        return "I'm having trouble processing your question. Please try again."
    except VectorStoreError:
        return "I'm unable to search the knowledge base right now. Please try later."
    except LLMError as e:
        logger.error(f"LLM error: {e}")
        return "I encountered an error generating a response. Please try again."
```

## Self-Check Validation

### Ingestion Quality
- [ ] Documents are chunked by semantic boundaries
- [ ] Metadata (source, headers) is preserved
- [ ] Chunk sizes are appropriate (500-1500 tokens)
- [ ] Overlap prevents context loss at boundaries

### Retrieval Quality
- [ ] Top-k results are relevant to test queries
- [ ] Similarity threshold filters low-quality matches
- [ ] Search latency is acceptable (<500ms)
- [ ] Edge cases (no results, many results) are handled

### Generation Quality
- [ ] Responses cite sources when appropriate
- [ ] Hallucinations are minimized
- [ ] Streaming provides responsive UX
- [ ] Error messages are user-friendly

### Production Readiness
- [ ] API rate limits are respected
- [ ] Connections are properly pooled
- [ ] Logging captures key metrics
- [ ] Monitoring alerts on failures
