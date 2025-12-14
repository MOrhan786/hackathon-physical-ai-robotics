---
id: 1
title: Initial Project Constitution Defined
stage: constitution
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude Code
command: /sp.constitution
labels: [constitution, project-setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ./.specify/memory/constitution.md
tests:

---

## Prompt

Act as the Lead Architect for the "Physical AI & Humanoid Robotics Textbook" project. We are winning a hackathon using the Spec-Kit Plus methodology.



Create a strict Project Constitution that defines the immutable standards for this project.



## 1. Project Vision & Scope

- **Goal:** Build an AI-native textbook platform that teaches Physical AI, ROS 2, and Isaac Sim.

- **Nature:** Hybrid project containing a Docusaurus frontend (the book) and a Python FastAPI backend (the RAG chatbot/agent).

- **Core Philosophy:** "Spec-First, AI-Augmented." We do not write code or chapters without a clear spec.



## 2. Technical Stack (Non-Negotiable)

- **Frontend/Content:** Docusaurus (React, TypeScript), MDX for content.

- **Backend/AI:** Python 3.12+ (managed via `uv`), FastAPI.

- **Database:** Neon Serverless Postgres (for logs/history), Qdrant (Vector DB).

- **Auth:** Better-Auth.

- **Orchestration:** Claude Code CLI + Spec-Kit Plus.



## 3. Global Quality Standards

- **Code (Python):**

  - Strict type hints (`mypy` compliant).

  - Google-style docstrings.

  - `pytest` for all backend logic.

- **Code (Frontend):**

  - TypeScript strict mode.

  - Components must be reusable (for buttons like "Translate" and "Personalize").

- **Content (Markdown):**

  - Every chapter must start with "Learning Outcomes."

  - Every chapter must end with "Assessments."

  - Structure must strictly follow the "Physical AI & Humanoid Robotics" syllabus modules.



## 4. Architecture & Methodology Rules

- **ADRs:** We must create an Architectural Decision Record (ADR) for:

  - The RAG retrieval logic.

  - The Urdu translation pipeline design.

  - The User Personalization data schema.

- **Checkpoints:** Work is performed in atomic tasks (<2 hours).

- **Validation:** No code is committed without passing tests; no content is committed without passing a "Curriculum Alignment" check.



## 5. Hackathon Constraints

- Speed is key, but stability is mandatory.

- The platform must support the 4 bonus features: RAG Chatbot, Auth, Personalization, and Urdu Translation.


Please generate the `constitution.md` file reflecting these rules.

## Response snapshot

The `constitution.md` file has been created, establishing the immutable standards for the "Physical AI & Humanoid Robotics Textbook" project.

**Version:** 1.0.0
**Rationale:** This is the initial creation of the project constitution.

**Files flagged for manual follow-up:**
While the template files (`plan-template.md`, `spec-template.md`, `tasks-template.md`, `adr-template.md`, `agent-file-template.md`, `checklist-template.md`, `phr-template.prompt.md`) were not directly modified in this process, their usage should now be aligned with the newly defined constitution. This means that future plans, specifications, tasks, ADRs, agent files, and checklists generated from these templates must adhere to the principles and guidelines outlined in the constitution.

**Suggested commit message:**
`docs: Initial project constitution v1.0.0 (principles, governance, and hackathon constraints defined)`

## Outcome

- ✅ Impact: Project constitution defined.
- 🧪 Tests: No tests were run for this action.
- 📁 Files: ./.specify/memory/constitution.md was created.
- 🔁 Next prompts: None, constitution creation is complete.
- 🧠 Reflection: The constitution was successfully created and the output summary was provided to the user. All templates for consistency propagation were reviewed, and a note about their pending alignment in usage was included in the sync report and summary.

## Evaluation notes (flywheel)

- Failure modes observed: Attempted to run a non-existent bash script for PHR creation, fell back to agent-native tools.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Ensure `create-phr.sh` script is available or update PHR creation instructions.
