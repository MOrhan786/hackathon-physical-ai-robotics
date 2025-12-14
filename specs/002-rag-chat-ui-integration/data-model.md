# Data Model: RAG Chatbot UI Integration

## 1. ChatMessage Entity

Represents a single message in a chat conversation.

-   **Name**: `ChatMessage`
-   **Description**: Stores the content, sender, and timestamp of a single chat message.
-   **Fields**:
    -   `id`: (Client-side generated UUID/timestamp for uniqueness, not persisted on backend)
    -   `text`: `string` (The actual content of the message)
    -   `sender`: `enum` (`'user'` or `'bot'`)
    -   `timestamp`: `ISO 8601 string` (e.g., `2023-10-27T10:00:00Z`)

## 2. ChatSession Entity

Represents a collection of chat messages for a continuous conversation. This entity will primarily be managed client-side for session persistence.

-   **Name**: `ChatSession`
-   **Description**: Aggregates `ChatMessage` entities to form a conversation history.
-   **Fields**:
    -   `id`: `string` (Unique identifier for the chat session, e.g., a UUID. Client-side generated)
    -   `messages`: `Array<ChatMessage>` (An ordered list of `ChatMessage` objects)
    -   `created_at`: `ISO 8601 string` (Timestamp when the session was initiated)
    -   `updated_at`: `ISO 8601 string` (Timestamp of the last message in the session)

## 3. Relationships

-   A `ChatSession` contains multiple `ChatMessage` entities.
