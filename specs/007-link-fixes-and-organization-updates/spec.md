# Feature Specification: Link Fixes and Organization Updates

**Feature ID**: 007-link-fixes-and-organization-updates  
**Created**: 2025-12-01  
**Status**: Completed  
**Priority**: High  

## Overview

Fix broken navigation links in the homepage, correct chatbot source links to include proper base URL for GitHub Pages deployment, and update footer organization links from Panaversity/PIAIC to BasenAI.

## Clarifications

### Session 2025-12-01
- Q: Which links are broken on the homepage? → A: Module 1 link uses `/docs/module-01/intro-physical-ai` instead of `/docs/module1/week1-intro-physical-ai`
- Q: What's wrong with chatbot source links? → A: Missing GitHub Pages base URL prefix (`/physical-ai-and-humanoid-robotics`)
- Q: What organization links should replace Panaversity/PIAIC? → A: BasenAI GitHub (https://github.com/orgs/basenai/dashboard) and LinkedIn (https://www.linkedin.com/company/basenai)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Homepage Navigation Links (Priority: P1)

As a visitor to the homepage, I want all module cards to navigate to the correct pages so that I can access the course content without encountering 404 errors.

**Why this priority**: Broken navigation links create a poor first impression and block access to content.

**Independent Test**: Click each module card on the homepage and verify it navigates to the correct module page.

**Acceptance Scenarios**:

1. **Given** the homepage is loaded, **When** clicking the "ROS 2 Fundamentals" module card, **Then** the system navigates to `/docs/module1/week1-intro-physical-ai`.
2. **Given** the homepage is loaded, **When** clicking the "View Modules" button in the hero section, **Then** the system navigates to `/docs/module1/week1-intro-physical-ai`.
3. **Given** the homepage is loaded, **When** clicking any module card, **Then** no 404 errors occur.

---

### User Story 2 - Chatbot Source Links (Priority: P1)

As a student using the AI chatbot, I want source links in chatbot responses to navigate to the correct documentation pages so that I can read the full context of the information provided.

**Why this priority**: Broken source links undermine trust in the chatbot and prevent users from accessing referenced content.

**Independent Test**: Ask the chatbot a question, receive a response with source links, and verify clicking the links navigates to the correct pages.

**Acceptance Scenarios**:

1. **Given** the chatbot provides a response with source links, **When** clicking a source link, **Then** the system navigates to the correct documentation page with the GitHub Pages base URL.
2. **Given** the chatbot references Module 1 content, **When** clicking the source link, **Then** the URL includes `/physical-ai-and-humanoid-robotics/docs/module1/...`.
3. **Given** the chatbot references the intro page, **When** clicking the source link, **Then** the URL is `/physical-ai-and-humanoid-robotics/docs`.

---

### User Story 3 - Footer Organization Links (Priority: P2)

As a visitor exploring the site, I want the footer to link to the correct organization (BasenAI) so that I can learn more about the team behind the project.

**Why this priority**: Accurate organization attribution is important for credibility and community building.

**Independent Test**: Scroll to the footer and verify the Community section links to BasenAI GitHub and LinkedIn.

**Acceptance Scenarios**:

1. **Given** the footer is visible, **When** viewing the Community section, **Then** the links display "BasenAI GitHub" and "BasenAI LinkedIn".
2. **Given** the footer is visible, **When** clicking "BasenAI GitHub", **Then** the system navigates to `https://github.com/orgs/basenai/dashboard`.
3. **Given** the footer is visible, **When** clicking "BasenAI LinkedIn", **Then** the system navigates to `https://www.linkedin.com/company/basenai`.

---

### Edge Cases

- What happens if the base URL changes in the future? → Update the `base_url` constant in `agent_service.py` and redeploy.
- How are anchor links handled in chatbot navigation? → The `_source_to_nav_path` function preserves anchor fragments in URLs.
- What if a source file doesn't match the expected pattern? → The function returns an empty string, and no navigation link is displayed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Homepage module cards MUST link to correct documentation paths matching the actual file structure.
- **FR-002**: Chatbot source links MUST include the GitHub Pages base URL (`/physical-ai-and-humanoid-robotics`).
- **FR-003**: Footer Community section MUST link to BasenAI organization pages (GitHub and LinkedIn).
- **FR-004**: All navigation links MUST be validated to prevent 404 errors.
- **FR-005**: The `_source_to_nav_path` function MUST construct URLs with the correct base URL prefix.

### Key Entities

- **Module Card**: Homepage component linking to a specific course module
- **Source Link**: Chatbot-generated link to documentation referenced in a response
- **Footer Link**: Navigation link in the site footer
- **Base URL**: GitHub Pages deployment path prefix (`/physical-ai-and-humanoid-robotics`)

## Out of Scope

- Automated link validation in CI/CD pipeline
- Redirects for old/deprecated URLs
- Link analytics or tracking
- Internationalization of organization links
- Dynamic base URL configuration from environment variables

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 4 homepage module cards navigate to correct pages (0 broken links).
- **SC-002**: Chatbot source links include correct base URL (100% of generated links).
- **SC-003**: Footer displays BasenAI links instead of Panaversity/PIAIC (2 links updated).
- **SC-004**: Manual testing confirms no 404 errors on homepage navigation.
- **SC-005**: Chatbot testing confirms source links navigate to correct pages.
- **SC-006**: Footer links open correct BasenAI organization pages.
