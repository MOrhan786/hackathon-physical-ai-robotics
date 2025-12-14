# Research Findings: RAG Chatbot UI Integration

## 1. Docusaurus Custom Component Integration

**Research Task**: Investigate the most idiomatic and maintainable way to add a custom React component (the floating button and chat interface) to the Docusaurus frontend. This includes understanding Docusaurus's lifecycle, theming overrides, and potential build process implications.

**Findings**:
Docusaurus provides several ways to extend and customize its UI:
1.  **Swizzling**: This allows "ejecting" and customizing existing Docusaurus components. While powerful, it can make upgrades harder. Not ideal for adding a completely new component.
2.  **Theming API (src/theme)**: This is the recommended approach for overriding or wrapping existing components, or creating new components that integrate with Docusaurus's styling. We can create new components within `src/theme` that use Docusaurus's theming context.
3.  **Custom Plugins/Presets**: For more complex integrations or to introduce new functionalities not directly related to existing theme components, a custom plugin or preset might be necessary. This is overkill for a chat widget.
4.  **Injecting custom React components via `src/css/custom.css` or `docusaurus.config.js`**: Less ideal for a fully interactive component as it bypasses React's typical component tree.

**Decision**: We will use the **Theming API (`src/theme`)** to integrate the custom React chat component. This allows us to create a new component (e.g., `src/theme/ChatWidget/index.js`) that is part of the Docusaurus React tree, benefiting from its build process and theming. A floating action button can be implemented as part of this component.

**Rationale**: This method offers the best balance of maintainability, integration with Docusaurus's build system, access to theming context, and flexibility to create a custom interactive component without heavily relying on swizzling.

**Alternatives Considered**:
-   Swizzling: Rejected due to potential upgrade difficulties.
-   Direct DOM manipulation: Rejected for being non-idiomatic React/Docusaurus.

## 2. Frontend Streaming Implementation

**Research Task**: Investigate the best practices and available libraries (if any are commonly used within Docusaurus/React context) for handling Server-Sent Events (SSE) or similar streaming protocols for the chatbot's responses.

**Findings**:
For handling streaming responses (specifically SSE) in a React application:
1.  **`EventSource` API**: This is a native browser API for handling SSE. It's straightforward to use and requires no external libraries. It emits events for incoming messages.
2.  **Third-party libraries**: While libraries exist (e.g., `axios-fetch-sse`), the native `EventSource` API is often sufficient for basic SSE handling in React. For more complex scenarios or polyfills for older browsers, a library might be considered.
3.  **React Hooks**: Custom React hooks can encapsulate the `EventSource` logic, making it reusable and easy to integrate into components.

**Decision**: We will utilize the native **`EventSource` API** encapsulated within a custom React hook to manage the streaming responses.

**Rationale**: `EventSource` is purpose-built for SSE, lightweight, and avoids additional dependencies. Encapsulating it in a hook provides a clean, reusable, and React-idiomatic solution.

**Alternatives Considered**:
-   WebSockets: Overkill for a read-only streaming scenario, introduces more complexity.
-   Polling: Inefficient for real-time streaming, introduces latency.
-   Third-party SSE libraries: Not necessary given the simplicity and robustness of the native `EventSource` API for our use case.

## 3. Text Selection & Context Passing

**Research Task**: Research how to efficiently capture user-selected text from Docusaurus content and pass it as context to the chat component and subsequently to the backend API.

**Findings**:
Capturing user-selected text in a web browser typically involves:
1.  **`window.getSelection()` API**: This native browser API allows getting the currently selected text and its range. It can be triggered by events like `mouseup` or `selectionchange`.
2.  **React `ref`s and event listeners**: A global event listener (e.g., on `document`) can capture selection events. The selected text can then be stored in React state.
3.  **Context API**: Once the text is captured, it can be passed down to the chat component using React Context, making it available throughout the component tree without prop drilling.

**Decision**: We will use the **`window.getSelection()` API** in conjunction with a global event listener (e.g., `mouseup`) to capture selected text. This selected text will then be stored in a React Context, making it accessible to the chat component for inclusion in API calls.

**Rationale**: This approach leverages native browser capabilities for selection and React's Context API for efficient state management across components, providing a clean and performant solution.

**Alternatives Considered**:
-   Manually copying and pasting: Poor user experience.
-   Docusaurus-specific selection plugins: No obvious out-of-the-box solution, would require custom development anyway.
