# Physical AI & Humanoid Robotics Textbook — Implementation Plan

**Version**: 1.0 (Reverse Engineered)
**Date**: 2026-02-19
**Spec Reference**: `specs/physical-ai-textbook/spec.md`

---

## Architecture Overview

**Architectural Style**: Static Site + Decoupled API (Jamstack)

**Reasoning**: Docusaurus generates static HTML/JS/CSS that can be deployed to any CDN (Vercel). The dynamic features (chat, personalization, translation, auth) are handled by a separate backend API. This separation allows:
- Frontend: Zero server cost, infinite scalability via CDN
- Backend: Independent scaling, can be deployed anywhere (Railway, HuggingFace, etc.)
- Content: Markdown files versioned in Git, easy to edit and extend

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                  │
│  ┌─────────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Docusaurus  │  │  React   │  │  CSS Modules  │  │
│  │   (SSG)      │  │Components│  │   (Styling)   │  │
│  └──────┬───────┘  └────┬─────┘  └───────────────┘  │
│         │               │                             │
│  ┌──────┴───────────────┴──────────────────────────┐ │
│  │              AuthContext (React Context)          │ │
│  │  ┌─────────┐ ┌──────────┐ ┌──────────────────┐  │ │
│  │  │ChatPanel│ │Personalzr│ │TranslationControl│  │ │
│  │  └────┬────┘ └─────┬────┘ └────────┬─────────┘  │ │
│  └───────┼────────────┼───────────────┼─────────────┘ │
└──────────┼────────────┼───────────────┼───────────────┘
           │            │               │
      ┌────┴────────────┴───────────────┴────┐
      │     REST API (HTTPS + CORS)           │
      └────┬────────────┬───────────────┬────┘
           │            │               │
┌──────────┼────────────┼───────────────┼───────────────┐
│          │   BACKEND (HuggingFace Spaces)             │
│  ┌───────┴───┐ ┌──────┴──────┐ ┌─────┴────────────┐  │
│  │ /api/chat │ │/api/personal│ │/api/translate     │  │
│  │  (RAG)    │ │   ize       │ │                   │  │
│  └───────────┘ └─────────────┘ └───────────────────┘  │
│  ┌─────────────────────────────────────────────────┐  │
│  │           /api/auth/* (signup/signin/signout)    │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

---

## Layer Structure

### Layer 1: Content Layer (Docusaurus Docs)
- **Responsibility**: Static textbook content, navigation, sidebar
- **Components**:
  - `docs/` — 13 weekly markdown files + hardware requirements + intro
  - `docs/module1-4/_category_.json` — Module organization
  - `sidebars.ts` — Sidebar navigation configuration
- **Technology**: Docusaurus MDX, Mermaid diagrams, Prism syntax highlighting

### Layer 2: Presentation Layer (React Components)
- **Responsibility**: Interactive UI components, state management
- **Components**:
  - `src/components/Chat/` — AI chatbot UI (ChatPanel, AiChatButton)
  - `src/components/AuthContext.tsx` — Authentication state provider
  - `src/components/ContentHighlight/` — Section highlighting
  - `src/theme/Navbar/` — Custom navbar with auth button
  - `src/theme/DocItem/` — Doc page enhancements (personalization, translation)
  - `src/pages/` — Homepage and static pages
- **Technology**: React 19, TypeScript, CSS Modules

### Layer 3: API Communication Layer
- **Responsibility**: Backend communication, error handling, caching
- **Components**:
  - `fetchWithTimeout()` — Timeout-wrapped fetch with CORS support
  - `src/config.ts` — API URL configuration
  - In-memory caching (Map) for personalization/translation
- **Technology**: Fetch API, AbortController

### Layer 4: Backend API (External)
- **Responsibility**: RAG processing, AI personalization, translation, auth
- **Current Deployment**: Railway
- **Target Deployment**: HuggingFace Spaces
- **Endpoints**: /api/chat, /api/personalize, /api/translate, /api/auth/*

---

## Design Patterns Applied

### Pattern 1: Context Provider (React Context API)
- **Location**: `src/components/AuthContext.tsx`
- **Purpose**: Global authentication state accessible from any component
- **Implementation**: AuthProvider wraps entire app, provides user, login, signup, logout, updateBackground

### Pattern 2: Composition via Docusaurus Swizzling
- **Location**: `src/theme/DocItem/Layout/index.tsx`, `src/theme/Navbar/index.tsx`
- **Purpose**: Extend Docusaurus default components without forking
- **Implementation**: Wrapper components that add controls bar (translation, personalization) to doc pages

### Pattern 3: Observer Pattern (State Synchronization)
- **Location**: `src/theme/DocItem/Layout/index.tsx`
- **Purpose**: Mutual exclusion between personalization and translation
- **Implementation**: Parent component tracks active state, passes callbacks for cross-component reset

### Pattern 4: Module-Level Cache (Singleton Map)
- **Location**: `Personalizer.tsx`, `TranslationControl.tsx`
- **Purpose**: Avoid redundant API calls for same content
- **Implementation**: `Map<string, string>` at module scope, keyed by pathname + background

### Pattern 5: Shared State via Module Exports
- **Location**: `TranslationControl.tsx` (getSharedOriginalContent, setSharedOriginalContent)
- **Purpose**: Share original DOM content between personalization and translation
- **Implementation**: Module-level variable with getter/setter exports

---

## Technology Stack

| Category | Choice | Rationale |
|----------|--------|-----------|
| **SSG Framework** | Docusaurus 3.9.2 | Hackathon requirement, great for docs sites |
| **UI Framework** | React 19 | Docusaurus dependency, modern hooks API |
| **Language** | TypeScript 5.6 | Type safety, better IDE support |
| **Styling** | CSS Modules | Scoped styles, no conflicts with Docusaurus |
| **Icons** | react-icons (Feather) | Lightweight, consistent icon set |
| **Markdown** | react-markdown | Chat response rendering |
| **Code Highlighting** | Prism React Renderer | Docusaurus default, GitHub/Dracula themes |
| **Frontend Deploy** | Vercel | Free tier, excellent DX, CDN |
| **Backend Deploy** | HuggingFace Spaces | Free tier, ML-friendly, Python support |

---

## Module Breakdown

### Module: Authentication (`src/components/AuthContext.tsx`)
- **Purpose**: User registration, login, session management, profile
- **Key Components**: AuthProvider, AuthContext
- **Dependencies**: localStorage (browser), backend /api/auth/*
- **Complexity**: Medium
- **State**: user, isLoading, sessionToken

### Module: Chat (`src/components/Chat/`)
- **Purpose**: RAG-based AI assistant for textbook Q&A
- **Key Components**: ChatPanel, AiChatButton
- **Dependencies**: AuthContext, backend /api/chat, react-markdown, react-icons
- **Complexity**: High (message management, API integration, redirect handling)
- **State**: messages, input, isLoading, error, panelSize

### Module: Personalization (`src/theme/DocItem/Personalizer.tsx`)
- **Purpose**: Adapt chapter content to user's experience level
- **Key Components**: Personalizer
- **Dependencies**: AuthContext, TranslationControl (shared state), backend /api/personalize
- **Complexity**: Medium (DOM manipulation, caching, state sync)
- **State**: isPersonalized, isLoading, error

### Module: Translation (`src/theme/DocItem/TranslationControl.tsx`)
- **Purpose**: Translate chapter content to Urdu
- **Key Components**: TranslationControl
- **Dependencies**: AuthContext, backend /api/translate
- **Complexity**: Medium (DOM manipulation, RTL support, caching)
- **State**: isTranslated, isLoading, error

### Module: Navigation & Layout (`src/theme/`)
- **Purpose**: Custom navbar, doc layout, content highlighting
- **Key Components**: Navbar, DocItemLayoutWrapper, UserProfileButton, ContentHighlight
- **Dependencies**: Docusaurus theme, AuthContext
- **Complexity**: Medium

### Module: Content (`docs/`)
- **Purpose**: 13-week textbook content
- **Key Files**: 15 markdown files (intro, hardware, 13 weeks)
- **Dependencies**: None (static markdown)
- **Complexity**: Content creation (high), technical (low)

---

## Deployment Strategy

### Frontend (Vercel)
1. Connect GitHub repository to Vercel
2. Build command: `npm run build`
3. Output directory: `build/`
4. Environment variables:
   - `REACT_APP_API_URL` → HuggingFace backend URL
   - `REACT_APP_API_KEY` → API key (should not be hardcoded)

### Backend (HuggingFace Spaces)
1. Create HuggingFace Space with Docker or Gradio
2. Deploy FastAPI/Flask backend with RAG pipeline
3. Configure CORS to allow Vercel domain
4. Set up environment variables for AI model keys

### Deployment Flow
```
Developer → git push → GitHub → Vercel auto-deploy (frontend)
                              → HuggingFace (backend - manual or CI)
```

---

## Improvement Opportunities

### Technical Improvements
- [ ] **Centralize API configuration** — Single source of truth for API URL/key
- [ ] **Extract shared utilities** — fetchWithTimeout, formatMarkdownContent (duplicated 3x)
- [ ] **Add error boundaries** — React error boundaries for graceful component failures
- [ ] **Implement proper env vars** — Remove hardcoded API keys from source code

### Architectural Improvements
- [ ] **Service layer abstraction** — Create `apiService.ts` for all backend calls
- [ ] **Better state management** — Consider useReducer for complex chat state
- [ ] **Streaming responses** — SSE for chat to show progressive responses

### Content Improvements
- [ ] **Interactive exercises** — Add code playgrounds for Python/ROS examples
- [ ] **Quiz system** — Interactive assessment with scoring
- [ ] **Progress tracking** — Track which chapters user has completed

---

## Risk Analysis

### Risk 1: Backend Availability
- **Probability**: Medium
- **Impact**: High — Chat, personalization, translation all fail
- **Mitigation**: Graceful error messages, retry mechanisms already in place
- **Kill Switch**: Frontend works as static textbook even without backend

### Risk 2: API Key Exposure
- **Probability**: High (already exposed)
- **Impact**: Medium — unauthorized API access
- **Mitigation**: Move to server-side proxy or environment variables

### Risk 3: HuggingFace Cold Starts
- **Probability**: High (free tier)
- **Impact**: Medium — 30-60s first request delay
- **Mitigation**: 60s timeout already configured, show loading states
