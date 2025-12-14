# Research: Gemini API Migration

**Feature**: `003-gemini-api-migration`
**Date**: 2024-12-19

## Research Questions

### Q1: What is the equivalent Gemini model for GPT-4o?

**Finding**: `gemini-1.5-flash` is the recommended model for chat completions.
- Fast response times suitable for streaming
- Good quality for educational content
- Supports function calling
- Lower cost than gemini-1.5-pro

**Alternative**: `gemini-1.5-pro` for higher quality but slower responses.

### Q2: What embedding model should replace text-embedding-3-small?

**Finding**: `models/text-embedding-004` is Gemini's latest embedding model.
- 768-dimensional embeddings (vs 1536 for OpenAI)
- Supports task_type parameter for optimization
- Use `retrieval_document` for document ingestion
- Use `retrieval_query` for query embedding

**Note**: Dimension difference requires Qdrant collection recreation or reindexing.

### Q3: How does Gemini streaming work?

**Finding**: Gemini supports native streaming via `stream=True` parameter.

```python
response = chat.send_message(message, stream=True)
for chunk in response:
    if chunk.text:
        yield chunk.text
```

**Compatibility**: Same SSE format can be maintained for frontend.

### Q4: How to handle conversation history in Gemini?

**Finding**: Gemini uses a different history format than OpenAI.

```python
# Gemini format
history = [
    {"role": "user", "parts": ["message"]},
    {"role": "model", "parts": ["response"]}
]
chat = model.start_chat(history=history)
```

**Note**: Role names differ: "assistant" → "model"

### Q5: How to configure Gemini API key?

**Finding**: Use `genai.configure()` at module level.

```python
import google.generativeai as genai
genai.configure(api_key=settings.GEMINI_API_KEY)
```

**Best Practice**: Configure once at service initialization.

## API Comparison

| Feature | OpenAI | Gemini |
|---------|--------|--------|
| Chat Model | gpt-4o | gemini-1.5-flash |
| Embedding Model | text-embedding-3-small | text-embedding-004 |
| Embedding Dimensions | 1536 | 768 |
| Streaming | stream=True | stream=True |
| History Role (AI) | assistant | model |
| Function Calling | tools parameter | tools parameter |
| Temperature | 0.0-2.0 | 0.0-2.0 |
| Max Tokens | max_tokens | max_output_tokens |

## Code Snippets

### Embedding Generation

```python
import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)

result = genai.embed_content(
    model="models/text-embedding-004",
    content=text,
    task_type="retrieval_document"
)
embedding = result['embedding']
```

### Chat Completion with Streaming

```python
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=history)

response = chat.send_message(message, stream=True)
for chunk in response:
    if chunk.text:
        yield chunk.text
```

### Generation Config

```python
response = model.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        max_output_tokens=8000
    )
)
```

## Migration Risks

### Risk 1: Embedding Dimension Mismatch
- **Issue**: Gemini embeddings are 768-dim vs OpenAI's 1536-dim
- **Impact**: Existing Qdrant vectors incompatible
- **Solution**: Re-ingest all documents after migration

### Risk 2: Response Style Differences
- **Issue**: Gemini may produce different response styles
- **Impact**: User experience may vary
- **Solution**: Adjust system prompts if needed

### Risk 3: Rate Limiting
- **Issue**: Gemini has different rate limits
- **Impact**: May hit limits under load
- **Solution**: Implement retry logic with exponential backoff

## References

- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Gemini Embedding Models](https://ai.google.dev/models/gemini#text-embedding)
- [Gemini Chat API](https://ai.google.dev/tutorials/python_quickstart)
