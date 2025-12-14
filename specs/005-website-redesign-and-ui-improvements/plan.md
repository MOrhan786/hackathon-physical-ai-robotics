# Implementation Plan: Website Redesign and UI Improvements

**Plan ID:** 005  
**Date:** 2025-11-30  
**Status:** ✅ Completed  

## Technical Context

### Current State
- Basic Docusaurus template with default styling
- RAG chatbot failing due to Qdrant API incompatibility
- Poor mobile experience and template-like appearance
- Scattered user management (separate auth button, theme toggle)

### Target State
- Modern, Claude Code-inspired design system
- Reliable RAG chatbot with proper vector retrieval
- Unified user profile management
- Mobile-first responsive design

## Architecture Decisions

### 1. Design System Architecture
**Decision**: Implement warm color palette with CSS custom properties

```css
:root {
  --ifm-color-primary: #c9a87c;
  --ifm-background-color: #faf9f7;
  --ifm-font-family-base: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
}
```

**Rationale**: Warm colors create welcoming learning environment; CSS properties enable easy theming.

### 2. RAG System Architecture
**Decision**: Pre-fetch context before LLM calls, use `query_points` API

```python
# Pre-fetch context approach
textbook_context = self._search_textbook(search_query)
user_context = self._get_user_context(user_id)
system_prompt = self._get_system_prompt(textbook_context, user_context, current_page)
```

**Rationale**: Ensures reliable retrieval; `query_points` is current Qdrant API.

### 3. Document Chunking Strategy
**Decision**: Semantic chunking (200-2000 chars, avg 1000)

**Rationale**: Larger chunks provide better context; reduced from 101 tiny chunks to 22 meaningful chunks.

### 4. User Interface Architecture
**Decision**: Unified UserProfileButton component with dropdown

**Components**:
- User avatar with initials
- Dark/light mode toggle
- Profile editing modal
- GitHub link integration
- Authentication flows

### 5. Chat Interface Architecture
**Decision**: Resizable chat panel with markdown rendering

**Features**:
- Three size presets (S/M/L)
- ReactMarkdown for proper formatting
- Smooth CSS transitions
- Mobile-responsive layout

## File Changes

### Frontend (physical-ai-textbook/)
| File | Change Type | Description |
|------|-------------|-------------|
| `src/css/custom.css` | Rewrite | Complete design system (500+ lines) |
| `src/pages/index.tsx` | Rewrite | Modern homepage with hero, modules, features |
| `src/pages/index.module.css` | Rewrite | Homepage-specific styles |
| `src/theme/Navbar/UserProfileButton.tsx` | Create | Unified user profile dropdown |
| `src/theme/Navbar/UserProfileButton.module.css` | Create | Profile button styles |
| `src/theme/Navbar/index.tsx` | Modify | Integrate UserProfileButton |
| `src/components/Chat/ChatPanel.tsx` | Modify | Add markdown, resizing |
| `src/components/Chat/ChatPanel.module.css` | Modify | Chat panel styles |
| `static/img/logo.svg` | Create | Custom robot logo |
| `docusaurus.config.ts` | Modify | Clean up navbar, fix Prism |

### Backend (rag_chatbot/)
| File | Change Type | Description |
|------|-------------|-------------|
| `src/services/vector_store_service.py` | Modify | Update to `query_points` API |
| `src/services/document_loader.py` | Modify | Semantic chunking |
| `src/services/agent_service.py` | Rewrite | OpenAI Agents SDK with pre-fetch |
| `src/api/chat.py` | Modify | User context headers |

## Risk Analysis

### Technical Risks
1. **API Compatibility**: Qdrant API changes → Updated to latest client
2. **Performance**: Large corpus → Optimized chunking and caching
3. **Mobile**: Complex UI → Mobile-first approach

### Mitigation Strategies
- Tested all API changes before deployment
- Monitored response times during development
- Validated on multiple device sizes

## Dependencies

- Qdrant Cloud (vector database)
- Google Gemini API (LLM)
- OpenAI Agents SDK (agent framework)
- ReactMarkdown (markdown rendering)

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| RAG System Fixes | 2 hours | ✅ Complete |
| UI Design System | 3 hours | ✅ Complete |
| Homepage Redesign | 1.5 hours | ✅ Complete |
| User Experience | 2 hours | ✅ Complete |
| Testing & QA | 1 hour | ✅ Complete |
| **Total** | **9.5 hours** | **✅ Complete** |
