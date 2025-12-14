# Specification: Website Redesign and UI Improvements

**Spec ID:** 005  
**Date:** 2025-11-30  
**Status:** Completed  
**Priority:** High  

## Overview

Complete redesign of the Physical AI & Humanoid Robotics textbook website from a basic Docusaurus template to a modern, professional documentation site inspired by Claude Code docs. This includes fixing RAG chatbot functionality, implementing responsive design, and creating a unified user experience.

## Objectives

### Primary Goals
1. **Modern Design System**: Implement Claude Code-inspired design with warm color palette
2. **RAG Chatbot Fixes**: Resolve vector database retrieval issues and improve response quality
3. **User Experience**: Create unified navigation and user profile management
4. **Content Optimization**: Improve document chunking and markdown rendering
5. **Responsive Design**: Ensure mobile-first responsive layout

### Secondary Goals
1. Remove all template/placeholder content
2. Implement proper caching for transformations
3. Add tooltips and micro-interactions
4. Optimize performance and loading times

## User Stories

### US1: Modern Visual Design
**User Story:** As a student, I want a modern, professional-looking textbook website, so that I have confidence in the quality of the educational content.

#### Acceptance Criteria
1. WHEN a user visits the site, THE Docusaurus_Site SHALL display a warm, professional color scheme (#c9a87c primary)
2. WHEN a user reads content, THE Typography_System SHALL use optimized fonts with 1.65 line height for readability
3. WHEN a user navigates, THE Navbar SHALL display a clean, minimal design with custom robot logo
4. WHEN a user views on mobile, THE Layout SHALL be fully responsive with touch-optimized interactions

### US2: RAG Chatbot Reliability
**User Story:** As a student, I want the AI chatbot to provide accurate, relevant answers, so that I can get help understanding course material.

#### Acceptance Criteria
1. WHEN a user asks a question, THE RAG_Backend SHALL retrieve relevant content using updated Qdrant `query_points` API
2. WHEN documents are chunked, THE Ingestion_System SHALL use semantic chunking (200-2000 chars) for better context
3. WHEN a response is generated, THE Chat_Interface SHALL render markdown properly with ReactMarkdown
4. WHEN a user wants more space, THE Chat_Panel SHALL be resizable (S/M/L sizes)

### US3: Unified User Profile
**User Story:** As a user, I want a unified profile dropdown, so that I can manage my account and preferences from one place.

#### Acceptance Criteria
1. WHEN a user clicks their avatar, THE UserProfileButton SHALL display a dropdown with all user options
2. WHEN a user toggles dark/light mode, THE Theme_Toggle SHALL be accessible from the profile dropdown
3. WHEN a user edits their profile, THE Profile_Modal SHALL allow updating background information
4. WHEN a user is logged out, THE Profile_Button SHALL show sign-in option

### US4: Homepage Redesign
**User Story:** As a visitor, I want an engaging homepage, so that I understand the value of the course immediately.

#### Acceptance Criteria
1. WHEN a user visits the homepage, THE Hero_Section SHALL display a clear value proposition with CTA buttons
2. WHEN a user scrolls, THE Module_Cards SHALL show all 4 course modules with direct navigation
3. WHEN a user views features, THE Feature_Section SHALL highlight key benefits with icons
4. THE Homepage SHALL NOT contain any template/placeholder content

## Technical Requirements

### Frontend Requirements
- **Framework**: Docusaurus v3 with React 19
- **Styling**: CSS Modules with custom properties
- **Typography**: System font stack with proper hierarchy
- **Color Scheme**: Warm brown/tan palette (#c9a87c primary)
- **Responsive**: Mobile-first breakpoints (480px, 768px, 996px)

### Backend Requirements
- **RAG System**: OpenAI Agents SDK with Gemini backend
- **Vector Database**: Qdrant with improved chunking (200-2000 chars)
- **Caching**: Response caching for transformations
- **API**: FastAPI with proper error handling

### Design System
- **Primary Color**: #c9a87c (warm brown)
- **Background**: #faf9f7 (light) / #1a1a1a (dark)
- **Typography**: -apple-system font stack
- **Border Radius**: 8px global, 12px for cards
- **Shadows**: Subtle with rgba(0,0,0,0.12) opacity

## Success Criteria

### Functional Requirements
- ✅ RAG chatbot retrieves relevant content from vector database
- ✅ User authentication and profile management works
- ✅ All navigation links work without 404 errors
- ✅ Responsive design works on all device sizes
- ✅ Dark/light mode toggle functions properly

### Performance Requirements
- ✅ Page load time < 3 seconds
- ✅ Chat response time < 5 seconds
- ✅ Smooth animations and transitions
- ✅ Efficient vector search (< 1 second)

## Deliverables

1. **Redesigned Frontend**: Updated CSS, homepage, navbar, user profile
2. **Improved RAG System**: Fixed vector search, better chunking, markdown rendering
3. **User Experience**: Unified navigation, resizable chat, mobile optimization
4. **Documentation**: Specs, ADRs, PHRs following project patterns
