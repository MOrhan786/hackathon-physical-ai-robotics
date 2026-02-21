# Physical AI Textbook — Reusable Intelligence

**Version**: 1.0 (Extracted from Codebase)
**Date**: 2026-02-19

---

## Overview

This document captures reusable intelligence embedded in the codebase — patterns, decisions, and expertise worth preserving for future development.

---

## Extracted Skills

### Skill 1: Docusaurus Theme Swizzling for Interactive Features

**Persona**: You are a frontend engineer extending Docusaurus with custom interactive components while preserving the default documentation experience.

**Questions before implementing**:
- Which Docusaurus component needs modification? (Navbar, DocItem, Layout)
- Should the extension wrap or replace the original?
- Does the feature need auth context or API access?
- How does it interact with existing Docusaurus features (dark mode, sidebar, ToC)?

**Principles**:
- **Always wrap, never replace**: Use `@theme-original` imports to wrap default components
- **Use CSS Modules**: Avoid global CSS conflicts with Docusaurus styles
- **Check `useIsBrowser()`**: SSR-safe — don't access window/document without this guard
- **Respect Docusaurus lifecycle**: Reset component state on `location.pathname` changes

**Implementation Pattern** (from `src/theme/DocItem/Layout/index.tsx`):
```tsx
import DocItemLayout from '@theme-original/DocItem/Layout';
import type { Props } from '@theme/DocItem/Layout';

export default function DocItemLayoutWrapper(props: Props): JSX.Element {
  return (
    <>
      <div className={styles.controlsBar}>
        {/* Custom controls here */}
      </div>
      <DocItemLayout {...props} />  {/* Original component preserved */}
    </>
  );
}
```

**When to apply**: Any Docusaurus site needing interactive features beyond static docs.

---

### Skill 2: DOM Content Transformation with Original Preservation

**Persona**: You are a frontend engineer implementing content transformation (personalization, translation) that modifies page DOM while allowing users to revert.

**Questions before implementing**:
- How many transformations can be active simultaneously?
- Should transformations be cached? (API calls are expensive)
- How to handle navigation between pages? (state cleanup)
- What's the source content format? (HTML, Markdown, plain text)

**Principles**:
- **Save original before modifying**: Store original innerHTML before any transformation
- **Mutual exclusion**: Only one transformation active at a time — reset the other first
- **Module-level shared state**: Use exported getters/setters for cross-component state
- **Cache aggressively**: Use Map keyed by `pathname + transformation_params`
- **Always use original for new transforms**: Never transform already-transformed content

**Implementation Pattern** (from `Personalizer.tsx` + `TranslationControl.tsx`):
```tsx
// Module-level shared state
let sharedOriginalContent: string | null = null;
export function getSharedOriginalContent() { return sharedOriginalContent; }
export function setSharedOriginalContent(content: string | null) { sharedOriginalContent = content; }

// In transformation handler:
const contentElement = document.querySelector('.theme-doc-markdown');

// 1. Save original (only once)
if (!getSharedOriginalContent()) {
  setSharedOriginalContent(contentElement.innerHTML);
}

// 2. Always transform from original
const originalText = new DOMParser()
  .parseFromString(getSharedOriginalContent(), 'text/html').body.textContent;

// 3. API call with original text
const result = await api.transform(originalText);

// 4. Cache result
cache.set(cacheKey, result);

// 5. Replace DOM
contentElement.innerHTML = formattedResult;
```

**When to apply**: Any content management system needing user-controlled content transformations.

---

### Skill 3: Mobile-Friendly Fetch with Timeout

**Persona**: You are a frontend engineer making API calls that work reliably across desktop and mobile browsers.

**Principles**:
- **Always use AbortController**: Prevent hanging requests
- **Explicit CORS mode**: Set `mode: 'cors'` and `credentials: 'omit'` for cross-origin
- **Distinguish error types**: Network errors vs timeouts vs server errors
- **Mobile-appropriate timeouts**: 30-60s (mobile networks are slower)
- **Clear timeout on success**: Prevent memory leaks

**Implementation Pattern** (from codebase — used 4x):
```tsx
async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeout: number = 60000
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      mode: 'cors',
      credentials: 'omit',
    });
    clearTimeout(timeoutId);
    return response;
  } catch (err) {
    clearTimeout(timeoutId);
    if (err instanceof Error && err.name === 'AbortError') {
      throw new Error('Request timed out.');
    }
    if (err instanceof Error && err.message.includes('Failed to fetch')) {
      throw new Error('Network error.');
    }
    throw err;
  }
}
```

**When to apply**: Any web app making cross-origin API calls, especially with mobile users.

---

### Skill 4: React Context for Authentication State

**Persona**: You are a frontend engineer implementing browser-based authentication with React Context for a static site.

**Principles**:
- **localStorage for persistence**: Session survives page refresh
- **Check `useIsBrowser()`**: SSR-safe — no localStorage on server
- **Separate login/signup flows**: Different data requirements
- **Provide updateBackground**: Allow profile editing without re-auth
- **Clear state on logout**: Both local state and localStorage
- **Type everything**: Interface for User, UserBackground, AuthContextType

**When to apply**: Any Docusaurus or static site needing user accounts.

---

### Skill 5: Markdown-to-HTML Conversion (Client-Side)

**Persona**: You are rendering markdown API responses as formatted HTML in a browser.

**Implementation Pattern** (from codebase):
```tsx
function formatMarkdownContent(content: string): string {
  let html = content
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^\s*[-*]\s+(.*$)/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>');

  html = html.replace(/(<li>.*?<\/li>)+/g, '<ul>$&</ul>');
  return html;
}
```

**Note**: For complex markdown, prefer `react-markdown` library (already used in ChatPanel). This regex approach is for quick rendering in DOM-injected content.

---

## Architecture Decision Records (Inferred)

### ADR-001: Custom Auth over better-auth

**Status**: Accepted (pragmatic decision)

**Context**: PDF hackathon requirements specify better-auth.com. Team implemented custom auth instead.

**Decision**: Use custom token-based authentication with React Context

**Rationale** (inferred):
1. Faster to implement custom auth for hackathon deadline
2. Full control over user background questions in signup flow
3. No dependency on third-party auth library
4. Simpler integration with existing backend

**Consequences**:
- **Positive**: Full control, simpler code, no external dependency
- **Negative**: Potential point deduction in hackathon, less secure than battle-tested library
- **Trade-off**: Speed over compliance

---

### ADR-002: Docusaurus over Next.js

**Status**: Accepted (requirement-driven)

**Context**: Need a documentation/textbook platform

**Decision**: Use Docusaurus 3.9.2

**Rationale**:
1. Hackathon requirement specifies Docusaurus
2. Built for documentation sites — perfect fit for textbook
3. Markdown-first content authoring
4. Built-in sidebar, search, versioning
5. React-based — can add interactive components

**Consequences**:
- **Positive**: Fast setup, great docs UX, markdown content
- **Negative**: SSG limitations for dynamic features, swizzling can be fragile

---

### ADR-003: Railway for Backend (Migrating to HuggingFace)

**Status**: Superseded (moving to HuggingFace)

**Context**: Need to host FastAPI backend with RAG pipeline

**Original Decision**: Deploy on Railway
**New Decision**: Migrate to HuggingFace Spaces

**Rationale for migration**:
1. HuggingFace free tier for ML workloads
2. Better AI/ML ecosystem integration
3. Community visibility

---

## Code Conventions Observed

### Naming
- **Files**: kebab-case for docs (`week1-intro-physical-ai.md`), PascalCase for components (`ChatPanel.tsx`)
- **CSS Modules**: camelCase class names (`styles.chatPanel`)
- **Constants**: UPPER_CASE (`API_URL`, `API_KEY`, `CHAT_MESSAGES_KEY`)
- **Interfaces**: PascalCase with descriptive names (`ChatPanelProps`, `UserBackground`)

### Component Structure
- Default exports for React components
- Props interface defined above component
- Hooks at top of component body
- Event handlers as arrow functions
- CSS Module imports as `styles`

### Error Handling
- try/catch with user-friendly error messages
- Error state displayed in UI with dismiss option
- Console.error for debugging
- Retry mechanism for transient failures

---

## Lessons Learned

### What Worked Well
1. **Docusaurus swizzling** — Clean extension without forking
2. **CSS Modules** — No style conflicts with Docusaurus theme
3. **React Context** — Simple, effective auth state management
4. **In-memory caching** — Avoided redundant API calls
5. **Content quality** — Textbook-grade material with code examples

### What Could Be Improved
1. **DRY violations** — fetchWithTimeout duplicated 4 times
2. **Security** — API key hardcoded in source code
3. **API URL management** — Different URLs in different files
4. **Testing** — Zero tests
5. **TypeScript strictness** — `(window as any)` used for cross-component communication

### What to Avoid
1. **Hardcoding secrets in frontend** — Always use env vars
2. **Module-level mutable state** — Can cause issues with HMR and SSR
3. **DOM manipulation in React** — `innerHTML` assignment bypasses React's virtual DOM
4. **Duplicating utility functions** — Extract to shared module immediately
