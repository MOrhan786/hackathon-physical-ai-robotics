# Physical AI & Humanoid Robotics Textbook — Tasks

**Version**: 1.0 (Reverse Engineered)
**Date**: 2026-02-19
**Spec Reference**: `specs/physical-ai-textbook/spec.md`
**Plan Reference**: `specs/physical-ai-textbook/plan.md`

---

## Overview

This task breakdown represents the implementation status — what's DONE and what's PENDING.

---

## Phase 1: Project Setup — COMPLETED

### Task 1.1: Docusaurus Project Initialization
- [x] Initialize Docusaurus project with classic preset
- [x] Configure TypeScript support
- [x] Setup custom CSS theme (custom.css)
- [x] Configure sidebars.ts for course structure
- [x] Configure docusaurus.config.ts (title, navbar, footer)
- **Files**: `package.json`, `docusaurus.config.ts`, `sidebars.ts`, `tsconfig.json`

### Task 1.2: Custom Theme Setup
- [x] Swizzle Navbar component for auth button integration
- [x] Swizzle DocItem/Layout for personalization/translation controls
- [x] Create custom CSS modules for all components
- [x] Setup dark/light mode toggle
- **Files**: `src/theme/Navbar/`, `src/theme/DocItem/`, `src/css/custom.css`

---

## Phase 2: Textbook Content — COMPLETED

### Task 2.1: Course Introduction & Overview
- [x] Write intro.md with course overview, modules, learning objectives
- [x] Write hardware-requirements.md with 4-tier budget system
- **Files**: `docs/intro.md`, `docs/hardware-requirements.md`

### Task 2.2: Module 1 — ROS 2 Fundamentals (5 weeks)
- [x] Week 1: Introduction to Physical AI — theory, code examples, assessments
- [x] Week 2: Sensors and Embodiment — LiDAR, cameras, IMUs, force sensors
- [x] Week 3: ROS 2 Architecture — nodes, topics, services, DDS
- [x] Week 4: ROS 2 Communication — services, actions, error handling
- [x] Week 5: ROS 2 Packages — launch files, parameters, build system
- **Files**: `docs/module1/week1-5*.md`

### Task 2.3: Module 2 — Digital Simulation (2 weeks)
- [x] Week 6: Gazebo simulation — URDF, SDF, physics
- [x] Week 7: Unity integration — sensor simulation, LiDAR, cameras
- **Files**: `docs/module2/week6-7*.md`

### Task 2.4: Module 3 — NVIDIA Isaac (3 weeks)
- [x] Week 8: Isaac platform overview — GPU parallelism, Isaac Sim
- [x] Week 9: Isaac ROS and VSLAM — stereo cameras, localization
- [x] Week 10: Sim-to-Real transfer — domain randomization, RL training
- **Files**: `docs/module3/week8-10*.md`

### Task 2.5: Module 4 — Humanoid Robotics (3 weeks)
- [x] Week 11: Kinematics — DH parameters, forward/inverse kinematics
- [x] Week 12: Manipulation — grasp planning, HRI safety
- [x] Week 13: Conversational Robotics — Whisper, GPT-4, VLA models
- **Files**: `docs/module4/week11-13*.md`

---

## Phase 3: Authentication — COMPLETED

### Task 3.1: AuthContext Implementation
- [x] Create AuthContext with React Context API
- [x] Implement signup with background profiling
- [x] Implement login with session token
- [x] Implement logout with server notification
- [x] Implement updateBackground for profile editing
- [x] localStorage persistence for session
- [x] Error handling with timeout (30s)
- **File**: `src/components/AuthContext.tsx`

### Task 3.2: User Profile UI
- [x] Create UserProfileButton component
- [x] Auth modal (login/signup forms)
- [x] Background questions in signup (programming, robotics, languages, hardware)
- [x] Edit profile modal
- [x] Dropdown menu (theme toggle, edit profile, GitHub, sign out)
- [x] Avatar with user initials
- [x] Form validation (email, password, name)
- **Files**: `src/theme/Navbar/UserProfileButton.tsx`, `UserProfileButton.module.css`

---

## Phase 4: RAG Chat — COMPLETED

### Task 4.1: ChatPanel Component
- [x] Full chat UI with messages list
- [x] Input area with send button
- [x] Thinking/loading states
- [x] Markdown rendering for AI responses
- [x] Error handling with retry
- [x] Clear chat functionality
- [x] Session storage persistence
- [x] Resizable panel (S/M/L)
- **Files**: `src/components/Chat/ChatPanel.tsx`, `ChatPanel.module.css`

### Task 4.2: AiChatButton (Floating)
- [x] Floating chat button on all pages
- [x] Selected text context support
- [x] Open/close toggle
- **Files**: `src/components/Chat/AiChatButton.tsx`, `AiChatButton.module.css`

### Task 4.3: Content Highlighting
- [x] Hash-based section highlighting
- [x] Smooth scroll with offset
- [x] Fade animation (3s)
- **Files**: `src/components/ContentHighlight/ContentHighlight.tsx`

---

## Phase 5: Personalization & Translation — COMPLETED

### Task 5.1: Content Personalization
- [x] Personalizer component with icon button
- [x] API integration (POST /api/personalize)
- [x] In-memory cache per page+background
- [x] Toggle original/personalized
- [x] Auth requirement check
- [x] Loading/error states
- **File**: `src/theme/DocItem/Personalizer.tsx`

### Task 5.2: Urdu Translation
- [x] TranslationControl component with globe icon
- [x] API integration (POST /api/translate)
- [x] RTL support for Urdu content
- [x] In-memory cache per page
- [x] Toggle English/Urdu
- [x] Auth requirement check
- **File**: `src/theme/DocItem/TranslationControl.tsx`

### Task 5.3: Controls Integration
- [x] DocItemLayoutWrapper with both controls
- [x] Mutual exclusion (only one active at a time)
- [x] Shared original content management
- [x] Reset on page navigation
- **File**: `src/theme/DocItem/Layout/index.tsx`

---

## Phase 6: Code Quality — PENDING

### Task 6.1: Centralize API Configuration
- [ ] Create single `src/utils/api.ts` with centralized URL and key
- [ ] Remove hardcoded API URLs from AuthContext, ChatPanel, Personalizer, TranslationControl
- [ ] Use environment variables for API key
- **Priority**: High
- **Impact**: Security, maintainability

### Task 6.2: Extract Shared Utilities
- [ ] Extract `fetchWithTimeout()` to `src/utils/fetch.ts` (currently duplicated 4x)
- [ ] Extract `formatMarkdownContent()` to `src/utils/markdown.ts` (duplicated 2x)
- **Priority**: Medium
- **Impact**: DRY, maintainability

### Task 6.3: Fix .gitignore
- [ ] Add `.docusaurus/` to .gitignore
- [ ] Remove tracked .docusaurus files from git
- **Priority**: Medium

---

## Phase 7: Deployment — PENDING

### Task 7.1: Deploy Frontend to Vercel
- [ ] Connect GitHub repo to Vercel
- [ ] Configure build command: `npm run build`
- [ ] Set output directory: `build/`
- [ ] Add environment variables (REACT_APP_API_URL)
- [ ] Verify deployment works
- **Priority**: Critical

### Task 7.2: Deploy Backend to HuggingFace
- [ ] Create HuggingFace Space
- [ ] Configure Docker/Gradio for FastAPI backend
- [ ] Set up CORS for Vercel domain
- [ ] Migrate from Railway to HuggingFace
- [ ] Update frontend API URLs to HuggingFace endpoint
- **Priority**: Critical

### Task 7.3: Update API URLs After Deployment
- [ ] Update `src/config.ts` with HuggingFace URL
- [ ] Update `docusaurus.config.ts` customFields
- [ ] Verify all features work with new backend URL
- **Priority**: Critical (depends on 7.1 + 7.2)

---

## Phase 8: Testing — PENDING

### Task 8.1: Component Tests
- [ ] Test AuthContext (login, signup, logout, updateBackground)
- [ ] Test ChatPanel (send message, retry, clear)
- [ ] Test Personalizer (toggle, cache, auth check)
- [ ] Test TranslationControl (toggle, RTL, auth check)
- **Priority**: Low (for hackathon), High (for production)

---

## Phase 9: SDD Artifacts — IN PROGRESS

### Task 9.1: Project Constitution
- [ ] Fill constitution.md with project-specific principles
- **Priority**: Medium

### Task 9.2: Prompt History Records
- [ ] Create PHR for this reverse engineering session
- [ ] Setup PHR workflow for future sessions
- **Priority**: Medium

---

## Summary

| Phase | Status | Tasks |
|-------|--------|-------|
| 1. Project Setup | COMPLETED | 2/2 |
| 2. Textbook Content | COMPLETED | 5/5 |
| 3. Authentication | COMPLETED | 2/2 |
| 4. RAG Chat | COMPLETED | 3/3 |
| 5. Personalization & Translation | COMPLETED | 3/3 |
| 6. Code Quality | PENDING | 0/3 |
| 7. Deployment | PENDING | 0/3 |
| 8. Testing | PENDING | 0/1 |
| 9. SDD Artifacts | IN PROGRESS | 0/2 |
| **TOTAL** | | **15/24 (63%)** |

**Core Features: 100% Complete**
**Polish & Deploy: Pending**
