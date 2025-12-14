# Implementation Plan: Foundation: Docusaurus Setup & UI Architecture

**Branch**: `1-docusaurus-ui-architecture` | **Date**: 2025-11-28 | **Spec**: specs/1-docusaurus-ui-architecture/spec.md
**Input**: Feature specification from `/specs/1-docusaurus-ui-architecture/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the technical steps to initialize the Docusaurus project and implement the foundational UI architecture, including custom components required for the hackathon bonus features (Auth, Translation, Personalization, AI Chat). The focus is on infrastructure setup, not textbook content generation.

## Technical Context

**Language/Version**: TypeScript, React, Python 3.12+ (for future backend)
**Primary Dependencies**: Docusaurus, Node.js, npm/yarn, (FastAPI for future backend)
**Storage**: N/A for this frontend setup phase
**Testing**: Frontend testing will include unit and integration tests for React components. Backend will use `pytest`.
**Target Platform**: Web (static site hosted via GitHub Pages)
**Project Type**: Hybrid web application (Docusaurus frontend, future Python FastAPI backend)
**Performance Goals**: `npm start` runs successfully within 5 minutes of project setup. Implement code splitting and lazy loading for custom components, and regularly analyze bundle size to optimize performance.
**Constraints**: Strict TypeScript usage, component reusability, adherence to Docusaurus conventions. Ensure SSR/SSG safety for all interactive components using `useIsBrowser` or `BrowserOnly` as needed, and ensure `AuthContext` hydration safety. Enforce strict type definitions, validate Docusaurus configuration schema, prioritize accessibility (A11y), and implement robust error handling in custom components.
**Scale/Scope**: Initial Docusaurus site with 4 module placeholders and 4 custom UI components.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Spec-First, AI-Augmented Development**: Passed. The specification was created and validated prior to planning.
- **II. Non-Negotiable Technical Stack**: Passed. The plan adheres to Docusaurus (React, TypeScript), and acknowledges the future Python 3.12+ FastAPI backend.
- **III. Rigorous Quality Standards**: Passed. Strict TypeScript usage, component reusability, and the commitment to unit/integration testing for frontend components are explicitly included in the plan, aligning with the Constitution's mandate for comprehensive testing.
- **IV. Structured Architecture & Methodology**: Passed. Architectural decisions for Auth state management and Docusaurus DocItem swizzling will be documented as ADRs. Atomic tasks will be broken down in `tasks.md`.
- **V. Hackathon-Driven Execution**: Passed. This plan prioritizes rapid setup and foundational elements for the bonus features, aligning with hackathon constraints.

All Constitution Check gates pass.

## Project Structure

### Documentation (this feature)

```text
specs/1-docusaurus-ui-architecture/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command) - Not needed for this plan
├── data-model.md        # Phase 1 output (/sp.plan command) - Not needed for this plan
├── quickstart.md        # Phase 1 output (/sp.plan command) - Not needed for this plan
├── contracts/           # Phase 1 output (/sp.plan command) - Not needed for this plan
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
. (repository root)
├── docs/                     # Docusaurus content (Modules 1-4 markdown files)
│   ├── module1/
│   │   └── week1-chapter1.md
│   ├── module2/
│   │   └── week3-chapter1.md
│   ├── module3/
│   │   └── week6-chapter1.md
│   └── module4/
│       └── week9-chapter1.md
├── blog/                     # Docusaurus blog content (if needed)
├── src/
│   ├── components/           # General React components (e.g., shared UI)
│   └── theme/                # Docusaurus swizzled components, custom layouts
│       ├── Navbar/
│       │   └── AuthButton.tsx
│       ├── DocItem/
│       │   └── Layout.tsx    # To inject TranslationControl, Personalizer
│       └── Layout.tsx        # To inject AiChatButton (FAB)
├── docusaurus.config.ts      # Docusaurus configuration
├── sidebars.ts               # Docusaurus sidebar configuration
├── package.json
├── tsconfig.json
├── backend/                  # Future FastAPI backend (Python)
│   ├── src/
│   └── tests/
└── tests/                    # Overall project tests (e.g., Playwright E2E for frontend)
```

**Structure Decision**: The project will adopt a hybrid structure with a `frontend/` (implicitly Docusaurus at root) and `backend/` separation. Docusaurus content resides in `docs/`, custom UI components will be developed in `src/theme` for Docusaurus swizzling and `src/components` for general use.

## Phases

1.  **Scaffolding:** Initialize Docusaurus project (`physical-ai-textbook`) with TypeScript and configure GitHub Pages deployment.
2.  **Structure:** Create the folder hierarchy (`module1/`, `module2/`, etc.) and placeholder `.md` files within `docs/` for Modules 1-4, ensuring auto-generated sidebar navigation.
3.  **State Layer:** Implement a dummy `AuthContext` using React Context to manage User Personalization/Login status, providing a basic context for UI components.
4.  **UI Components:** Build the four React components:
    *   `AuthButton.tsx` (Navbar)
    *   `TranslationControl.tsx` (Top of Doc page)
    *   `Personalizer.tsx` (Top of Doc page)
    *   `AiChatButton.tsx` (Floating action button, bottom-right)
5.  **Integration:** Inject the custom UI components into the Docusaurus Layout. This will involve swizzling `DocItem` for `TranslationControl` and `Personalizer`, and modifying the main `Layout` for `AuthButton` and `AiChatButton`.

## Architectural Decisions (ADRs) to Record

- **ADR for React Context for Auth State Management**: Document the decision to use React Context for managing authentication and personalization state, outlining alternatives considered (e.g., Redux, Zustand) and the rationale for choosing Context for initial simplicity and hackathon speed.
- **ADR for Docusaurus UI Component Integration Strategy**: Document the decision on how to integrate UI components, specifically evaluating a plugin-first approach for `TranslationControl` and `Personalizer` versus swizzling, and justifying swizzling for `AuthButton` and `AiChatButton`. This ADR will detail the trade-offs, alternatives considered (e.g., custom plugins, direct DOM manipulation), and the rationale for the chosen Docusaurus extension mechanism for each component.
