---
title: "Skill: Docusaurus React Frontend"
version: "1.0.0"
description: "Patterns and best practices for building interactive React components within Docusaurus, including SSR safety, state management, and API integration."
created: "2025-11-30"
---

# Skill: Docusaurus React Frontend

## Persona
**Role:** You are a Senior Frontend Engineer specializing in React within static site generators.
**Cognitive Stance:**
- You understand that Docusaurus builds run in Node.js where browser APIs don't exist.
- You think in terms of hydration—server-rendered HTML must match client-rendered output.
- You balance between rich interactivity and build-time safety.
- You prioritize user experience: fast loads, responsive interactions, graceful errors.

## Analytical Questions (The Checklist)
Before finalizing any Docusaurus React implementation, ask:

1. **SSR Safety:** Does this component access window/document/localStorage safely?
2. **Hydration:** Will server and client render the same initial HTML?
3. **State Management:** Is state properly scoped and persisted where needed?
4. **API Integration:** Are loading/error states handled? Is streaming working?
5. **Accessibility:** Are ARIA labels provided? Is keyboard navigation supported?
6. **Performance:** Are heavy components lazy-loaded? Is re-rendering minimized?
7. **Type Safety:** Are all props and state properly typed with TypeScript?

## Decision Principles

### 1. SSR/SSG Safety
- **Guard Browser APIs:** Always check for browser environment before accessing window/document.
- **Use Docusaurus Hooks:** `useIsBrowser()`, `BrowserOnly`, `ExecutionEnvironment`.
- **Avoid Hydration Mismatches:** Don't render different content on server vs client.

```typescript
import useIsBrowser from '@docusaurus/useIsBrowser';
import BrowserOnly from '@docusaurus/BrowserOnly';

function SafeComponent() {
  const isBrowser = useIsBrowser();
  
  if (!isBrowser) {
    return <div className="skeleton">Loading...</div>;
  }
  
  const savedData = localStorage.getItem('key');
  return <div>{savedData}</div>;
}

function ComponentWithBrowserOnly() {
  return (
    <BrowserOnly fallback={<div>Loading...</div>}>
      {() => {
        const width = window.innerWidth;
        return <div>Window width: {width}</div>;
      }}
    </BrowserOnly>
  );
}
```

### 2. State Management
- **Local State:** Use useState for component-specific state.
- **Context:** Use React Context for shared state across components.
- **Session Storage:** Persist state across page navigations within session.
- **Avoid Global State:** Don't use window globals; they break SSR.

```typescript
const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const isBrowser = useIsBrowser();
  
  useEffect(() => {
    if (!isBrowser) return;
    const saved = sessionStorage.getItem('user');
    if (saved) setUser(JSON.parse(saved));
  }, [isBrowser]);
  
  useEffect(() => {
    if (!isBrowser) return;
    if (user) {
      sessionStorage.setItem('user', JSON.stringify(user));
    } else {
      sessionStorage.removeItem('user');
    }
  }, [user, isBrowser]);
  
  return (
    <AuthContext.Provider value={{ user, isAuthenticated: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
```

### 3. API Integration
- **Fetch with Error Handling:** Always handle network errors gracefully.
- **Loading States:** Show feedback during async operations.
- **SSE Streaming:** Parse Server-Sent Events correctly.
- **Abort Controllers:** Cancel requests on unmount.

```typescript
const sendMessage = async (message: string) => {
  setIsLoading(true);
  setError(null);
  
  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
      body: JSON.stringify({ message }),
    });
    
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    let content = '';
    
    if (reader) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        for (const line of chunk.split('\n')) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data && data !== '[DONE]') {
              content += data;
              setStreamingContent(content);
            }
          }
        }
      }
    }
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Request failed');
  } finally {
    setIsLoading(false);
  }
};
```

### 4. Docusaurus Navigation
- **Use Docusaurus Router:** Don't use window.location for internal navigation.
- **Base URL Handling:** Account for baseUrl in all internal links.
- **Preserve State:** Use session storage to persist state across navigations.

```typescript
import { useHistory } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';

function NavigationComponent() {
  const history = useHistory();
  const baseUrl = useBaseUrl('/');
  
  const navigateTo = (path: string) => {
    const fullUrl = baseUrl.endsWith('/')
      ? baseUrl.slice(0, -1) + path
      : baseUrl + path;
    history.push(fullUrl);
  };
  
  return (
    <button onClick={() => navigateTo('/docs/module-01')}>
      Go to Module 1
    </button>
  );
}
```

### 5. Theme Customization
- **Swizzle Carefully:** Prefer wrapping over ejecting components.
- **CSS Modules:** Use .module.css for scoped styles.
- **CSS Variables:** Use Docusaurus CSS variables for theming.

```typescript
import React from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';
import CustomControls from '../CustomControls';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): JSX.Element {
  return (
    <>
      <CustomControls />
      <Layout {...props} />
    </>
  );
}
```

### 6. CSS Modules Pattern
```typescript
import styles from './Component.module.css';

function StyledComponent({ isActive }: { isActive: boolean }) {
  return (
    <div className={styles.container}>
      <button className={`${styles.button} ${isActive ? styles.active : ''}`}>
        Click me
      </button>
    </div>
  );
}
```

## Self-Check Validation

### SSR Safety
- [ ] No direct window/document access without guards
- [ ] useIsBrowser() or BrowserOnly used appropriately
- [ ] No hydration mismatch warnings in console
- [ ] Build completes without errors

### State Management
- [ ] State is properly typed with TypeScript
- [ ] Side effects are in useEffect with cleanup
- [ ] Context providers wrap appropriate component trees
- [ ] Session/local storage access is guarded

### API Integration
- [ ] Loading states shown during requests
- [ ] Errors caught and displayed to users
- [ ] Streaming responses update UI incrementally
- [ ] Requests cancelled on component unmount

### Code Quality
- [ ] TypeScript strict mode passes
- [ ] No `any` types without justification
- [ ] CSS modules used for component styles
- [ ] Accessibility attributes provided
