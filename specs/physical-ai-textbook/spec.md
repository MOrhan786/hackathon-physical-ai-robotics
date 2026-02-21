# Physical AI & Humanoid Robotics Textbook — Specification

**Version**: 1.0 (Reverse Engineered)
**Date**: 2026-02-19
**Source**: Hackathon I PDF + Existing Codebase
**Feature**: physical-ai-textbook

---

## Problem Statement

Students and professionals need a comprehensive, interactive textbook for learning Physical AI & Humanoid Robotics — covering ROS 2, Gazebo, NVIDIA Isaac, and conversational robotics. Traditional textbooks lack interactivity, personalization, and AI-assisted learning. This project creates an AI-native educational platform that adapts to each learner's background.

## System Intent

**Target Users**: Students, robotics enthusiasts, professionals learning Physical AI
**Organization**: Panaversity (panaversity.org)

**Core Value Proposition**: An interactive, AI-powered textbook that personalizes content based on user background (programming experience, robotics knowledge, hardware access) and provides a RAG-based AI assistant for real-time learning support.

**Key Capabilities**:
1. 13-week structured textbook content with code examples and assessments
2. RAG-based AI chatbot for context-aware Q&A on book content
3. User authentication with background profiling for personalization
4. Per-chapter content personalization based on user experience level
5. Per-chapter Urdu translation for accessibility
6. Hardware requirements guide with tiered budget options

---

## Functional Requirements

### FR-1: Docusaurus-Based Textbook Website
- **What**: Static site built with Docusaurus containing 13 weeks of course material organized in 4 modules
- **Why**: Hackathon requirement #1 — create a textbook for Physical AI & Humanoid Robotics
- **Structure**:
  - Module 1 (Weeks 1-5): The Robotic Nervous System (ROS 2)
  - Module 2 (Weeks 6-7): The Digital Twin (Gazebo & Unity)
  - Module 3 (Weeks 8-10): The AI-Robot Brain (NVIDIA Isaac)
  - Module 4 (Weeks 11-13): Vision-Language-Action (VLA) & Conversational Robotics
- **Content per week**: Theory, code examples (Python/XML/Bash), mermaid diagrams, assessment questions
- **Success Criteria**: All 13 weeks have detailed, textbook-quality content with working code examples

### FR-2: RAG ChatKit (AI Assistant)
- **What**: Floating AI chatbot that answers questions based on textbook content using RAG
- **Why**: Hackathon requirement #3 — implement RAG-based chat
- **Inputs**: User message, optional selected text from page, chat history
- **Outputs**: AI-generated response in markdown format
- **Features**:
  - Floating button on all pages
  - Resizable panel (S/M/L)
  - Session-persistent message history (sessionStorage)
  - Context-aware: uses selected text as context
  - Markdown rendering for responses
  - Navigation/redirect support (can direct users to relevant sections)
  - Retry on failure
  - Clear chat functionality
- **API**: POST `/api/chat` with message, history, selected_text
- **Success Criteria**: Chatbot responds accurately about textbook content, supports context selection

### FR-3: User Authentication (Signup/Signin)
- **What**: User registration and login with background profiling
- **Why**: Hackathon requirement #5 (bonus) — implement auth with user background questions
- **Signup Inputs**: email, password, name, background (programming_experience, robotics_experience, preferred_languages, hardware_access)
- **Login Inputs**: email, password
- **Outputs**: Session token, user object
- **Features**:
  - Form validation (email format, password strength 6+ chars with upper/lowercase)
  - Session persistence via localStorage
  - User profile editing (update background)
  - Logout with server notification
  - Error handling with timeout (30s)
- **API Endpoints**:
  - POST `/api/auth/signup`
  - POST `/api/auth/signin`
  - POST `/api/auth/signout`
- **Success Criteria**: Users can register with background info, login, edit profile, logout
- **Note**: PDF specifies better-auth.com — current implementation uses custom auth

### FR-4: Content Personalization
- **What**: Per-chapter content adaptation based on user's programming/robotics experience
- **Why**: Hackathon requirement #6 (bonus) — personalize content per chapter
- **Inputs**: Chapter content (text), user background
- **Outputs**: Personalized content HTML
- **Features**:
  - Button at top of each doc page
  - Requires authentication
  - Caches personalized content per page+background
  - Toggle between original and personalized
  - Loading states and error handling
  - Mutual exclusion with translation (only one active at a time)
- **API**: POST `/api/personalize` with content, user_background
- **Success Criteria**: Logged-in user can personalize any chapter based on their background

### FR-5: Urdu Translation
- **What**: Per-chapter content translation to Urdu
- **Why**: Hackathon requirement #7 (bonus) — translate content to Urdu per chapter
- **Inputs**: Chapter content (text), target_language="urdu"
- **Outputs**: Translated content HTML with RTL support
- **Features**:
  - Globe icon button at top of each doc page
  - Requires authentication
  - Caches translated content per page
  - Toggle between English and Urdu
  - RTL (Right-to-Left) text direction for Urdu
  - Mutual exclusion with personalization
  - Banner: "اردو میں ترجمہ شدہ"
- **API**: POST `/api/translate` with content, target_language
- **Success Criteria**: Logged-in user can translate any chapter to Urdu with proper RTL rendering

### FR-6: Hardware Requirements Chapter
- **What**: Dedicated page detailing hardware requirements for the course
- **Why**: Hackathon requirement #4 — include hardware requirements
- **Content**:
  - 4-tier budget system (Cloud $50-200/mo, Workstation $3-5K, Edge $700-2K, Full Lab $16K+)
  - Specific product recommendations with pricing
  - Cloud provider comparison (AWS, Azure, GCP, Lambda Labs)
  - Desktop build guide (~$2,300)
  - NVIDIA driver and CUDA installation scripts
  - Assessment questions
- **Success Criteria**: Comprehensive, actionable hardware guide with current pricing

### FR-7: Homepage & Navigation
- **What**: Landing page with course overview, module cards, and structured navigation
- **Why**: User orientation and course discoverability
- **Features**:
  - Hero section with course tagline
  - Module cards linking to respective weeks
  - Navbar with "Start Learning" link and "Modules" dropdown
  - Footer with course links, community links, GitHub
  - Dark/light mode toggle (via user profile dropdown)
- **Success Criteria**: Clear, professional landing page that guides users to content

### FR-8: Content Highlighting
- **What**: Visual highlighting of content sections when navigating via chat redirects
- **Why**: Enhanced UX for AI-assisted navigation
- **Features**:
  - Smooth scrolling to content anchors
  - Visual highlight overlay with fade animation (3s duration)
  - 100px scroll offset for better visibility
  - Responds to URL hash changes
- **Success Criteria**: When chat redirects to a section, that section is visually highlighted

---

## Non-Functional Requirements

### Performance
- **Chat Response**: < 60s timeout (API call to RAG backend)
- **Page Load**: Static site generation via Docusaurus for fast loading
- **Caching**: In-memory cache for personalization and translation results
- **Session**: localStorage for auth, sessionStorage for chat messages

### Security
- **Authentication**: Custom token-based auth (session tokens)
- **API Key**: X-API-Key header for backend communication
- **CORS**: Explicit CORS mode with credentials omitted
- **Input Validation**: Client-side form validation (email format, password strength)
- **Known Risk**: API key hardcoded in frontend (`password123`) — should use environment variables

### Reliability
- **Fetch Timeout**: 30s for auth, 60s for chat/personalize/translate
- **Error Recovery**: Retry mechanism on chat failures
- **Graceful Degradation**: Fallback to localhost for development
- **Session Persistence**: Auth survives page refresh (localStorage)

### Accessibility
- **ARIA Labels**: On all interactive buttons
- **Semantic HTML**: Proper heading hierarchy in content
- **RTL Support**: For Urdu translation
- **Keyboard Navigation**: Enter to send chat messages

### Scalability
- **Frontend**: Static site (infinitely scalable via CDN)
- **Backend**: Decoupled API (can scale independently)
- **Content**: Markdown-based (easy to add new weeks/modules)

---

## System Architecture

### Frontend (This Repository)
- **Framework**: Docusaurus 3.9.2 (React 19+)
- **Language**: TypeScript
- **Styling**: CSS Modules + custom theme
- **State Management**: React Context (AuthContext)
- **Routing**: Docusaurus built-in routing

### Backend (External — Railway)
- **Production URL**: `simple-hackathon-physical-ai-and-humanoid-roboti-production.up.railway.app`
- **Alt URL**: `web-production-e1ceb.up.railway.app`
- **API Endpoints**:
  - `POST /api/chat` — RAG chatbot
  - `POST /api/personalize` — Content personalization
  - `POST /api/translate` — Content translation
  - `POST /api/auth/signup` — User registration
  - `POST /api/auth/signin` — User login
  - `POST /api/auth/signout` — User logout

### Deployment Target (Updated)
- **Frontend**: Vercel (static site)
- **Backend**: HuggingFace Spaces

---

## External Dependencies

| Dependency | Version | Purpose |
|-----------|---------|---------|
| @docusaurus/core | 3.9.2 | Static site framework |
| @docusaurus/preset-classic | 3.9.2 | Default Docusaurus preset |
| react | ^19.0.0 | UI framework |
| react-dom | ^19.0.0 | React DOM rendering |
| react-icons | ^5.3.0 | Icon components (FiSend, FiX, etc.) |
| react-markdown | ^9.0.1 | Markdown rendering in chat |
| clsx | ^2.0.0 | Conditional classnames |
| prism-react-renderer | ^2.3.0 | Code syntax highlighting |
| typescript | ~5.6.2 | Type safety |

---

## Known Gaps & Technical Debt

### Gap 1: API Key Hardcoded
- **Issue**: `API_KEY = 'password123'` hardcoded in multiple files
- **Files**: `AuthContext.tsx:8`, `ChatPanel.tsx:38`, `Personalizer.tsx:9`, `TranslationControl.tsx:8`
- **Impact**: Security vulnerability — API key visible in client bundle
- **Recommendation**: Move to environment variables, use Docusaurus customFields

### Gap 2: better-auth Not Used
- **Issue**: PDF requires better-auth.com for authentication
- **Impact**: Potential point deduction in hackathon evaluation
- **Recommendation**: Consider migrating to better-auth or document reason for custom auth

### Gap 3: No Tests
- **Issue**: Zero test files in the project
- **Impact**: No confidence in code correctness, fragile to changes
- **Recommendation**: Add component tests for critical features (auth, chat, personalization)

### Gap 4: Duplicate fetchWithTimeout
- **Issue**: `fetchWithTimeout` function duplicated across 4 files
- **Impact**: Code maintenance burden, inconsistent changes
- **Recommendation**: Extract to shared utility module

### Gap 5: API URL Inconsistency
- **Issue**: Different API URLs across files (with/without https://, different hostnames)
- **Files**: `config.ts`, `AuthContext.tsx`, `ChatPanel.tsx`, `Personalizer.tsx`
- **Impact**: Possible connection failures, confusion
- **Recommendation**: Centralize API URL in single config source

### Gap 6: .docusaurus Tracked in Git
- **Issue**: Build artifacts tracked in version control
- **Impact**: Noisy diffs, merge conflicts
- **Recommendation**: Add `.docusaurus/` to `.gitignore`

---

## Success Criteria

### Functional Success
- [x] All 13 weeks of content present and detailed
- [x] RAG chatbot functional with context-aware responses
- [x] User authentication with background profiling
- [x] Content personalization per chapter
- [x] Urdu translation per chapter
- [x] Hardware requirements chapter included
- [x] Navigation and homepage complete
- [ ] better-auth integration (PDF requirement — not met)
- [ ] Deployment on Vercel + HuggingFace (pending)

### Non-Functional Success
- [x] Mobile-friendly with CORS support
- [x] Error handling on all API calls
- [x] Cache for personalization/translation
- [ ] Test coverage > 0%
- [ ] No hardcoded secrets

---

## Acceptance Tests

### Test 1: Chat Assistant
**Given**: User is on any textbook page
**When**: User clicks chat button, types "What is ROS 2?", presses Enter
**Then**: AI responds with relevant information from textbook content

### Test 2: Signup with Background
**Given**: User is not logged in
**When**: User clicks profile icon, fills signup form with name/email/password/background, submits
**Then**: Account created, user logged in, background saved

### Test 3: Content Personalization
**Given**: User is logged in with "beginner" programming experience
**When**: User navigates to Week 3 (ROS Fundamentals), clicks Personalize button
**Then**: Content is adapted for beginner level with simpler explanations

### Test 4: Urdu Translation
**Given**: User is logged in on any chapter page
**When**: User clicks Translation (globe) button
**Then**: Content translated to Urdu with RTL layout

### Test 5: Chat Context Selection
**Given**: User selects text "NVIDIA Isaac Sim" on a page
**When**: User opens chat and asks "Explain this"
**Then**: Chat responds with information specifically about NVIDIA Isaac Sim
