# Feature Specification: RAG Vector Retrieval Fix

**Feature Branch**: `004-rag-vector-retrieval-fix`  
**Created**: 2025-11-30  
**Status**: Completed  
**Input**: User description: "The chatbot isn't retrieving data from the vector database properly"

## User Scenarios & Testing

### User Story 1 - Vector Database Search Integration (Priority: P1)

As a student using the Physical AI textbook chatbot, I want the AI to search and retrieve relevant content from the vector database when I ask questions, so that I receive accurate answers based on the actual textbook content.

**Why this priority**: Core RAG functionality - without proper vector retrieval, the chatbot cannot provide textbook-specific answers.

**Independent Test**: Ask "What does module 2 cover?" and verify the response includes specific textbook content about Gazebo & Unity simulation.

**Acceptance Scenarios**:

1. **Given** a user asks about Module 2, **When** the chatbot processes the query, **Then** it should search the vector database and return content about Gazebo, Unity, physics simulation, and sensors.
2. **Given** the vector search returns results, **When** generating a response, **Then** the AI should cite source files and relevance scores.
3. **Given** no relevant content is found, **When** generating a response, **Then** the AI should clearly state the answer is from general knowledge.

---

### User Story 2 - User Context Personalization (Priority: P2)

As a logged-in student, I want the chatbot to personalize responses based on my background (programming experience, robotics experience, preferred languages), so that explanations match my skill level.

**Why this priority**: Enhances learning experience by adapting content complexity to user's background.

**Independent Test**: Login as a user with "intermediate programming" background and ask about ROS 2 - response should reference Python/rclpy and provide appropriate complexity.

**Acceptance Scenarios**:

1. **Given** a logged-in user with intermediate programming experience, **When** asking about ROS 2, **Then** the response should include Python code examples and reference rclpy.
2. **Given** a user with no robotics experience, **When** asking about URDF, **Then** the response should provide beginner-friendly explanations.
3. **Given** an anonymous user, **When** asking questions, **Then** the response should be suitable for all experience levels.

---

### User Story 3 - Current Page Context Awareness (Priority: P3)

As a student browsing the textbook, I want the chatbot to know which page I'm currently viewing, so that it can provide contextually relevant answers.

**Why this priority**: Improves user experience by providing page-aware responses.

**Independent Test**: Navigate to Module 1 intro page and ask a question - the chatbot should acknowledge the current page context.

**Acceptance Scenarios**:

1. **Given** a user is on `/docs/module-1/intro`, **When** asking a question, **Then** the chatbot should be aware of the current page context.
2. **Given** page context is provided, **When** generating responses, **Then** the AI should prioritize content relevant to the current page.

---

### Edge Cases

- What happens when the vector database is unavailable? → Return error message gracefully
- What happens when user background data is incomplete? → Fall back to general responses
- What happens when embedding service fails? → Log error and provide general knowledge response

## Requirements

### Functional Requirements

- **FR-001**: System MUST use OpenAI Agents SDK function tools for vector database search
- **FR-002**: System MUST retrieve user context from database when user_id is provided
- **FR-003**: System MUST pass current page URL to the agent for context awareness
- **FR-004**: System MUST include source file references and relevance scores in search results
- **FR-005**: System MUST handle search errors gracefully without crashing
- **FR-006**: Frontend MUST send X-User-ID and X-Current-Page headers with chat requests

### Key Entities

- **TextbookAgent**: Main agent class with search and user context tools
- **search_textbook**: Function tool for vector database queries
- **get_user_context**: Function tool for retrieving user background
- **ChatRequest**: Request model with message, history, and selected_text

## Success Criteria

### Measurable Outcomes

- **SC-001**: Chatbot returns textbook-specific content when asked about course modules
- **SC-002**: Responses include source citations with relevance scores
- **SC-003**: Logged-in users receive personalized responses based on their background
- **SC-004**: Current page context is reflected in response relevance
