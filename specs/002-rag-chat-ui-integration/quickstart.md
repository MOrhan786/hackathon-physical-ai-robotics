# Quickstart Guide: RAG Chatbot UI Integration

This guide provides a rapid setup and deployment process for integrating the RAG Chatbot UI component into a Docusaurus project.

## Prerequisites

-   An existing Docusaurus project (version 2.x or 3.x).
-   Node.js (LTS) and npm/yarn installed.
-   Access to the RAG Chatbot Backend API endpoint and a valid API key.

## 1. Add the Chat Component

The chat interface will be implemented as a custom React component within your Docusaurus project's `src/theme` directory.

### 1.1. Create the Component Files

Create the following directory structure and placeholder files within your Docusaurus project:

```
src/theme/
└── ChatWidget/
    ├── index.js          # Main Chat Widget component
    ├── ChatWindow.js     # Component for the chat conversation window
    ├── ChatButton.js     # Component for the floating chat button
    ├── ChatMessage.js    # Component for displaying individual messages
    ├── ChatInput.js      # Component for the message input field
    └── useChatStream.js  # Custom hook for handling API streaming
```

### 1.2. Implement Core Logic

**(This step is conceptual and details will be covered in subsequent tasks)**

-   **`ChatButton.js`**: A React component for the floating button. It will manage the visibility state of the `ChatWindow`.
-   **`ChatWindow.js`**: The main component that renders the chat conversation, input, and handles state for messages.
-   **`ChatMessage.js`**: Displays a single message, distinguishing between user and bot.
-   **`ChatInput.js`**: Handles user input and sends messages to the API.
-   **`useChatStream.js`**: A custom React hook that encapsulates the `EventSource` API logic for streaming responses from the RAG backend.
-   **`index.js`**: Orchestrates the `ChatButton` and `ChatWindow` components, potentially using React Context for global state like selected text.

### 1.3. Integrate into Docusaurus Layout

To make the chat widget available globally, you will need to extend the default Docusaurus layout.

1.  **Swizzle the Layout component (if not already done)**:
    ```bash
    npx @docusaurus/theme-common swizzle @docusaurus/theme-classic Layout --wrap
    ```
    This will create `src/theme/Layout/index.js` (or similar).

2.  **Modify `src/theme/Layout/index.js`**:
    Import and render your `ChatWidget` component.

    ```javascript
    import React from 'react';
    import Layout from '@theme-init/Layout';
    import ChatWidget from '../ChatWidget'; // Adjust path as necessary

    export default function LayoutWrapper(props) {
      return (
        <>
          <Layout {...props} />
          <ChatWidget />
        </>
      );
    }
    ```

## 2. Configure API Key

The API key for the RAG chatbot backend will be managed as an environment variable during the Docusaurus build process.

1.  **Create a `.env` file** in the root of your Docusaurus project (if one doesn't exist).

2.  **Add your API key** to the `.env` file:

    ```
    REACT_APP_RAG_API_KEY=your_super_secret_api_key_here
    ```
    *(Note: Docusaurus, being a React-based framework, often uses `REACT_APP_` prefix for client-side environment variables.)*

3.  **Access the API key** in your React components:

    ```javascript
    const RAG_API_KEY = process.env.REACT_APP_RAG_API_KEY;
    // Use RAG_API_KEY in your fetch requests
    ```

## 3. Build and Serve Docusaurus

1.  **Install dependencies**:
    ```bash
    npm install # or yarn install
    ```

2.  **Start the development server**:
    ```bash
    npm start # or yarn start
    ```
    Your Docusaurus site with the integrated chat widget will be available, typically at `http://localhost:3000`.

3.  **Build for production**:
    ```bash
    npm run build # or yarn build
    ```
    The build output will be in the `build/` directory.

## Next Steps

This quickstart provides the basic setup. Further development will involve implementing the detailed UI/UX for the chat window, handling API interactions, state management, and robust error handling.
