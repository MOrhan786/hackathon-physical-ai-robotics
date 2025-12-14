---
id: 5
title: Foundation Docusaurus Setup & UI Architecture Spec
stage: spec
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: docusaurus-ui-architecture
branch: 1-docusaurus-ui-architecture
user: Claude Code
command: "Foundation: Docusaurus Setup & UI Architecture" I need a specification for the *software foundation* of our Physical AI Textbook. DO NOT generate textbook content yet. Focus only on the infrastructure.
labels: [spec, docusaurus, ui-architecture, frontend]
links:
  spec: specs/1-docusaurus-ui-architecture/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-docusaurus-ui-architecture/spec.md
  - specs/1-docusaurus-ui-architecture/checklists/requirements.md
tests:

---

## Prompt

"Foundation: Docusaurus Setup & UI Architecture" I need a specification for the *software foundation* of our Physical AI Textbook. DO NOT generate textbook content yet. Focus only on the infrastructure.



## 1. Goal



Initialize the Docusaurus project and create the specific UI components required for the Hackathon bonus features.



## 2. Platform Requirements



- **Initialize:** Create a new Docusaurus site (`physical-ai-textbook`) using TypeScript.

- **Theme:** Clean, academic, high-contrast. Title: "Physical AI & Humanoid Robotics".

- **Navigation (Sidebar):**

    - Create the *file structure* (folders and placeholder `.md` files) for Modules 1, 2, 3, and 4 exactly as per the syllabus.

    - Sidebar must auto-generate from these folders.



## 3. Required Custom UI Components (The "Bonus" Shells)



We need to create React components for the hackathon requirements. These will be "dumb" components for now (UI only, logic later).



- **`AuthButton.tsx`**: A button in the Navbar. Text: "Login".

- **`TranslationControl.tsx`**: A button at the top of every Doc page. Text: "Translate to Urdu".

- **`Personalizer.tsx`**: A toggle/button at the top of every Doc page. Text: "Personalize Content".

- **`AiChatButton.tsx`**: A floating action button (bottom-right). Icon: Chat bubble.



## 4. Acceptance Criteria



- `npm start` runs successfully.

- Sidebar shows the correct hierarchy (Module 1 -> Weeks -> Chapters).

- Clicking a chapter opens a page (even if with dummy content).

- The 4 custom components (Login, Translate, Personalize, Chat) are visible on the site.

- The project is committed to GitHub Pages deployment workflow.



## 5. Constitution Check



- Ensure strict TypeScript usage.

- Ensure component reusability (Dry Principle).

## Response snapshot

The specification for "Foundation: Docusaurus Setup & UI Architecture" has been successfully created and validated.

- **Branch Name**: `1-docusaurus-ui-architecture`
- **Specification File**: `specs/1-docusaurus-ui-architecture/spec.md`
- **Checklist Results**: All items passed in `specs/1-docusaurus-ui-architecture/checklists/requirements.md`.

This feature is now ready for the planning phase.

## Outcome

- ✅ Impact: Feature specification created, validated, and ready for planning.
- 🧪 Tests: Specification quality checklist passed.
- 📁 Files: `specs/1-docusaurus-ui-architecture/spec.md` and `specs/1-docusaurus-ui-architecture/checklists/requirements.md` were created and updated.
- 🔁 Next prompts: User can now proceed with `/sp.plan`.
- 🧠 Reflection: Successfully handled the script failure by falling back to agent-native tools, created all required artifacts, and validated the spec.

## Evaluation notes (flywheel)

- Failure modes observed: Initial script execution failed due to `pwsh` not found.
- Graders run and results (PASS/FAIL): All checklist items passed after one iteration of updates to the spec.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Incorporate a check for `pwsh` availability and provide instructions for its installation if missing.
