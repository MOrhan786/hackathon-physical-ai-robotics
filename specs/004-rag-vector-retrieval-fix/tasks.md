# Implementation Tasks: RAG Vector Retrieval Fix

**Feature**: 004-rag-vector-retrieval-fix  
**Created**: 2025-11-30  
**Status**: Completed

## Phase 1: Backend Agent Refactoring

- [x] T001 Refactor agent_service.py to use OpenAI Agents SDK function tools
  - Create `_create_search_tool()` method with `@function_tool` decorator
  - Implement vector search logic inside the tool
  - Return formatted context with source citations
  - _Requirements: FR-001, FR-004_

- [x] T002 Create user context function tool
  - Create `_create_user_context_tool()` method
  - Retrieve user background from database
  - Format user context for agent consumption
  - _Requirements: FR-002_

- [x] T003 Update TextbookAgent initialization
  - Initialize agent with both function tools
  - Update system prompt with tool usage instructions
  - Configure model with Gemini backend
  - _Requirements: FR-001, FR-002_

- [x] T004 Modify chat_stream method
  - Use Runner.run() for agent execution
  - Pass enhanced message with context
  - Handle streaming response
  - _Requirements: FR-001_

## Phase 2: API Endpoint Updates

- [x] T005 Update chat endpoint to accept context headers
  - Add X-User-ID header parameter
  - Add X-Current-Page header parameter
  - Pass headers to agent service
  - _Requirements: FR-003, FR-006_

## Phase 3: Frontend Integration

- [x] T006 Update ChatPanel to send context headers
  - Add user.id to X-User-ID header when authenticated
  - Add window.location.pathname to X-Current-Page header
  - Ensure headers are only sent when values exist
  - _Requirements: FR-006_

## Phase 4: Validation

- [x] T007 Test vector retrieval functionality
  - Query about Module 2 content
  - Verify response includes textbook-specific information
  - Confirm source citations are present
  - _Requirements: SC-001, SC-002_

- [x] T008 Test user context personalization
  - Login as user with known background
  - Ask about ROS 2 learning path
  - Verify response is personalized to user's experience level
  - _Requirements: SC-003_

- [x] T009 Test current page context
  - Set X-Current-Page header to module path
  - Verify agent acknowledges page context
  - _Requirements: SC-004_

## Completion Summary

All tasks completed successfully. The RAG chatbot now:
- Searches vector database using function tools
- Retrieves user context for personalization
- Accepts current page context via headers
- Returns comprehensive, personalized responses with source citations
