# Research: RAG Vector Retrieval Fix

**Feature**: 004-rag-vector-retrieval-fix  
**Created**: 2025-11-30

## Problem Analysis

### Root Cause

The original implementation was not using the vector search as a tool for the agent. Instead, it was attempting to use the agent without proper RAG integration, resulting in:
- Responses based on general knowledge only
- No textbook-specific content in answers
- Missing source citations

### Investigation Findings

1. **Agent Service Structure**: The agent was initialized but not configured with function tools for vector search
2. **Missing Tool Integration**: OpenAI Agents SDK requires explicit function tools for external data access
3. **Context Passing**: User context and page information were not being passed to the agent

## Solution Research

### OpenAI Agents SDK Function Tools

The OpenAI Agents SDK provides the `@function_tool` decorator for creating tools that agents can use:

```python
from agents import function_tool

@function_tool
def search_textbook(query: str) -> str:
    """Search the Physical AI textbook for relevant content."""
    # Implementation
    return context
```

Key findings:
- Tools must be synchronous (not async)
- Return type should be string for text-based responses
- Docstring is used as tool description for the agent

### Gemini OpenAI-Compatible Endpoint

The project uses Gemini via OpenAI-compatible endpoint:

```python
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

client = AsyncOpenAI(
    api_key=settings.GEMINI_API_KEY,
    base_url=settings.GEMINI_BASE_URL  # https://generativelanguage.googleapis.com/v1beta/openai/
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)
```

### Vector Search Integration

The existing vector store service provides search functionality:

```python
results = self.vector_store_service.search_vectors(embedding, limit=5)
```

Results include:
- `text`: The chunk content
- `source_file`: Original file path
- `score`: Relevance score (0-1)

## Implementation Approach

### Function Tool Pattern

```python
def _create_search_tool(self):
    @function_tool
    def search_textbook(query: str) -> str:
        """Search the Physical AI textbook for relevant content."""
        try:
            embedding = self.embedding_service.get_embedding(query)
            results = self.vector_store_service.search_vectors(embedding, limit=5)
            
            if not results:
                return "No relevant content found."
            
            context = "TEXTBOOK CONTENT:\n\n"
            for i, result in enumerate(results, 1):
                context += f"--- Source {i}: {result['source_file']} (Relevance: {result['score']:.2f}) ---\n"
                context += f"{result['text']}\n\n"
            
            return context
        except Exception as e:
            return f"Error searching textbook: {str(e)}"
    
    return search_textbook
```

### Agent Configuration

```python
self.agent = Agent(
    name="Physical AI Textbook Assistant",
    instructions=self._get_system_prompt(),
    model=self.model,
    tools=[self.search_tool, self.user_context_tool]
)
```

### System Prompt Updates

The system prompt must instruct the agent to use tools:

```
IMPORTANT INSTRUCTIONS:
1. ALWAYS use the search_textbook tool to find relevant content before answering questions
2. Use the get_user_context tool to personalize responses based on user's background
3. Base your answers primarily on the retrieved textbook content
```

## Validation Results

### Test 1: Module 2 Query

**Query**: "What does module 2 cover? Tell me in depth"

**Result**: ✅ Success
- Response included detailed content about Gazebo & Unity
- Source citations present with relevance scores
- Covered physics simulation, sensors, URDF/SDF formats

### Test 2: Personalized Learning Path

**Query**: "How should I approach learning ROS 2 as a beginner?"
**User Context**: Intermediate programming, Python knowledge, no robotics experience

**Result**: ✅ Success
- Response acknowledged user's Python background
- Recommended rclpy for Python development
- Provided step-by-step learning path appropriate for skill level

### Test 3: URDF for Humanoids

**Query**: "I'm working on a humanoid robot project. What should I know about URDF for humanoids?"

**Result**: ✅ Success
- Comprehensive response with code examples
- Personalized to user's intermediate programming level
- Included Python integration examples with rclpy

## Conclusions

1. **Function tools are essential** for proper RAG integration with OpenAI Agents SDK
2. **Synchronous tool execution** works well for vector search operations
3. **System prompt instructions** are critical for guiding agent tool usage
4. **Header-based context passing** is clean and maintainable
5. **Error handling in tools** prevents agent failures from propagating
