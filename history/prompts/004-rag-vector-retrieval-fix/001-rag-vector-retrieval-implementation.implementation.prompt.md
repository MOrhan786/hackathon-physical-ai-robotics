---
id: 001
title: RAG Vector Retrieval Implementation
stage: implementation
date: 2025-11-30
surface: agent
model: claude-sonnet-4-20250514
feature: 004-rag-vector-retrieval-fix
branch: main
user: kk
command: implementation
labels: ["rag", "vector-search", "function-tools", "openai-agents-sdk", "personalization"]
links:
  spec: specs/004-rag-vector-retrieval-fix/spec.md
  ticket: null
  adr: history/adr/004-rag-function-tools.md
  pr: null
files:
  - rag_chatbot/src/services/agent_service.py
  - rag_chatbot/src/api/chat.py
  - physical-ai-textbook/src/components/Chat/ChatPanel.tsx
tests:
  - Vector retrieval test with Module 2 query
  - User context personalization test
  - URDF humanoid query test
---

## Prompt

The chatbot isn't retrieving data from the vector database properly. Fix this by implementing proper RAG functionality with OpenAI Agents SDK and function tools. The issue is that the current implementation isn't using the vector search as a tool for the agent.

## Response snapshot

Implemented complete RAG functionality fix for the Physical AI textbook chatbot:

### Technical Changes Made:

1. **agent_service.py - Complete Rewrite**
   - Created `_create_search_tool()` method with `@function_tool` decorator
   - Implemented vector search logic returning formatted context with source citations
   - Created `_create_user_context_tool()` for user background retrieval
   - Updated TextbookAgent initialization with both function tools
   - Modified system prompt with explicit tool usage instructions
   - Updated `chat_stream()` to use `Runner.run()` for agent execution

2. **chat.py - Header Support**
   - Added `X-User-ID` header parameter for user identification
   - Added `X-Current-Page` header parameter for page context
   - Updated endpoint to pass context to agent service

3. **ChatPanel.tsx - Frontend Integration**
   - Added user context headers to fetch request
   - Added current page URL to X-Current-Page header
   - Conditional header inclusion based on authentication state

### Validation Tests Performed:

**Test 1: Module 2 Query**
- Query: "What does module 2 cover? Tell me in depth"
- Result: ✅ Comprehensive response about Gazebo & Unity, physics simulation, sensors
- Source citations included with relevance scores

**Test 2: Personalized Learning Path**
- Query: "How should I approach learning ROS 2 as a beginner?"
- User: Intermediate programming, Python knowledge, no robotics experience
- Result: ✅ Personalized response with Python/rclpy focus, step-by-step learning path

**Test 3: URDF for Humanoids**
- Query: "I'm working on a humanoid robot project. What should I know about URDF?"
- Result: ✅ Detailed response with code examples, personalized to user's skill level

### Key Architecture Decisions:

- Used synchronous function tools (OpenAI Agents SDK requirement)
- Header-based context passing for clean API design
- Error handling inside tools to prevent agent failures
- System prompt instructs agent to always use search tool first

## Outcome

- ✅ Impact: RAG chatbot now properly retrieves and uses vector database content
- 🧪 Tests: All 3 validation tests passed - vector search, personalization, context awareness
- 📁 Files: 3 files modified (agent_service.py, chat.py, ChatPanel.tsx)
- 🔁 Next prompts: Deploy backend, update frontend API URLs for production
- 🧠 Reflection: Function tools are essential for proper RAG integration with OpenAI Agents SDK

## Evaluation notes (flywheel)

- Failure modes observed: None - all tests passed
- Graders run and results (PASS/FAIL): Vector retrieval PASS, Personalization PASS, Context awareness PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add caching for frequently asked questions
