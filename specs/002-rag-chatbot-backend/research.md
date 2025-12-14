# Research & Decisions: RAG Chatbot Backend

This document records key decisions made during the clarification phase for the RAG Chatbot Backend feature.

## 1. API Security Mechanism

-   **Decision**: A static, pre-shared API key is required for all backend endpoints.
-   **Rationale**: This approach provides a necessary layer of security to prevent unauthorized public access, fitting the project's scope without introducing the complexity of a full user authentication system. It's a standard and effective pattern for protecting internal or non-user-facing APIs.
-   **Alternatives Considered**:
    -   *No Security*: Rejected as it would leave the API vulnerable.
    -   *CORS Origin Control*: Rejected as it's a browser-level security feature and provides no protection against server-to-server requests.

## 2. Behavior for No Found Documents

-   **Decision**: If the vector search yields no relevant documents, the system will forward the user's question to the LLM without context and prepend the response with a disclaimer.
-   **Rationale**: This provides a graceful fallback, ensuring the user still gets a response. The disclaimer manages expectations by clarifying that the answer is from the LLM's general knowledge, not the specific course material, thus mitigating the risk of perceived inaccuracy.
-   **Alternatives Considered**:
    -   *Static "Not Found" Message*: A safe but less helpful option. The chosen approach provides more value to the user.
    -   *Suggest Rephrasing*: Adds complexity to implementation and may not always be effective.

## 3. Mid-Stream API Failure Handling

-   **Decision**: If the connection to the OpenAI API fails mid-stream, the system will attempt to append a structured error message to the response stream.
-   **Rationale**: This provides the best user experience by explicitly informing the user of a server-side error. It is more transparent than a silent failure or an abruptly truncated message.
-   **Alternatives Considered**:
    -   *Silent Failure*: Rejected as it creates a confusing and poor user experience.
    -   *Log and Drop*: Rejected for the same reason as silent failure; the user is left unaware of the error.
