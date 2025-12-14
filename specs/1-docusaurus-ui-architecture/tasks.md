---
description: "Task list for Docusaurus UI Architecture feature implementation"
---

**Note on Task Duration Estimates**: According to the project constitution (Section IV, "Checkpoints"), all tasks should have an estimated duration of less than 2 hours. While not explicitly provided for each task below, this is a critical guideline for future task breakdown and tracking.

# Tasks: Foundation: Docusaurus Setup & UI Architecture

**Input**: Design documents from `/specs/1-docusaurus-ui-architecture/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested for this feature, focusing on functional verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: Docusaurus is implicitly at the repository root.

## Phase 1: Setup (Scaffolding)

**Purpose**: Project initialization and basic structure

- [X] T001 [<1h] Initialize Docusaurus project `physical-ai-textbook` with TypeScript in the root directory (Command provided: `npx create-docusaurus physical-ai-textbook classic --typescript --git`).
- [X] T002 [<1h] Configure Docusaurus for GitHub Pages deployment workflow in `docusaurus.config.ts`.

---

## Phase 2: Foundational (Structure and State Layer)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

⚠️ **CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 [<1h] Create `docs/module1/`, `docs/module2/`, `docs/module3/`, `docs/module4/` directories.
- [X] T004 [<1h] Create placeholder markdown files for Modules 1-4 (e.g., `docs/module1/week1-chapter1.md`) based on the syllabus detailed in `specs/course-details/spec.md`.
- [X] T005 [P] [<1h] Implement dummy `AuthContext` (React Context) in `src/components/AuthContext.tsx`.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Initial Docusaurus Site Setup (Priority: P1) 🎯 MVP

**Goal**: Docusaurus site is initialized with basic structure, theme, and navigation.

**Independent Test**: The Docusaurus site can be started locally, and the basic structure and theme are visible.

### Implementation for User Story 1

- [X] T006 [US1] [<1h] Verify `npm start` runs successfully and the site is accessible.
- [X] T007 [US1] [<1h] Verify the title "Physical AI & Humanoid Robotics" is displayed in `docusaurus.config.ts`.
- [ ] T008 [US1] [<1h] Verify sidebar auto-generates navigation from `docs/` module folders in `sidebars.ts`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Custom UI Component Integration (Priority: P1)

**Goal**: Required custom UI components are integrated into the Docusaurus site.

**Independent Test**: All four custom components are visibly present on the Docusaurus site in their specified locations.

### Implementation for User Story 2

- [ ] T009 [P] [US2] [<1h] Create `AuthButton.tsx` component in `src/theme/Navbar/AuthButton.tsx`.
- [ ] T010 [P] [US2] [<1h] Create `TranslationControl.tsx` component in `src/theme/DocItem/TranslationControl.tsx`.
- [ ] T011 [P] [US2] [<1h] Create `Personalizer.tsx` component in `src/theme/DocItem/Personalizer.tsx`.
- [ ] T012 [P] [US2] [<1h] Create `AiChatButton.tsx` component in `src/theme/Layout/AiChatButton.tsx`.
- [ ] T013 [US2] [<1h] Swizzle Docusaurus Navbar to inject `AuthButton` into `src/theme/Navbar/AuthButton.tsx`.
- [ ] T014 [US2] [<1h] Swizzle Docusaurus `DocItem` layout to inject `TranslationControl` and `Personalizer` into `src/theme/DocItem/Layout.tsx`.
- [ ] T015 [US2] [<1h] Customize the main Docusaurus `Layout` to inject `AiChatButton` (floating action button) into `src/theme/Layout.tsx`.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T016 [<1h] Implement unit tests for `AuthButton.tsx`, `TranslationControl.tsx`, `Personalizer.tsx`, and `AiChatButton.tsx` in `src/components/__tests__/`.
- [ ] T017 [<1h] Run all frontend unit tests.
- [ ] T018 [<1h] Implement SSR/SSG safety for interactive custom components using `useIsBrowser` or `BrowserOnly` as needed.
- [ ] T019 [<1h] Ensure `AuthContext` is safely hydrated for SSR/SSG environments.
- [ ] T020 [<1h] Implement code splitting and lazy loading for custom components to optimize bundle size.
- [ ] T021 [<1h] Perform Docusaurus configuration schema validation.
- [ ] T022 [<1h] Prioritize accessibility (A11y) for all custom UI components.
- [ ] T023 [<1h] Implement robust error handling mechanisms within custom UI components.
- [ ] T024 [<1h] Verify strict TypeScript usage across all new and modified frontend files.
- [ ] T025 [<1h] Verify component reusability for custom UI components.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 (e.g., using AuthContext) but should be independently testable for its UI components.

### Within Each User Story

- Component creation tasks (T009-T012) can be done in parallel before integration tasks.
- Integration tasks (T013-T015) are sequential as they modify shared layout files.

### Parallel Opportunities

- T005 (AuthContext) can be done in parallel with T003-T004 (Module Structure).
- T009-T012 (UI Components creation) can run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Scaffolding
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Scaffolding + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
