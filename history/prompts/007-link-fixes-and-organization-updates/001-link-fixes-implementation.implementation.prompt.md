---
id: 001
title: Link Fixes Implementation
stage: implementation
date: 2025-12-01
surface: agent
model: claude-sonnet-4-20250514
feature: 007-link-fixes-and-organization-updates
branch: main
user: kk
command: implementation
labels: ["bug-fix", "navigation", "links", "footer", "chatbot"]
links:
  spec: specs/007-link-fixes-and-organization-updates/spec.md
  ticket: null
  adr: history/adr/007-link-fixes-base-url-strategy.md
  pr: null
files:
  - docs/src/pages/index.tsx
  - backend/src/services/agent_service.py
  - docs/docusaurus.config.ts
tests:
  - getDiagnostics validation (all files passed)
---

## Prompt

1. some of the buttons in the home page redirect to not found pages, fix them, 2. when the chatbot gives links to sources, they are mostly broken links lead to not  found pages fix them, 3. change the panaversity and piaic links in the footer to my organization links: https://github.com/orgs/basenai/dashboard, https://www.linkedin.com/company/basenai.

## Response snapshot

Fixed three categories of broken/incorrect links:

### 1. Homepage Navigation Links
**Problem**: Module 1 card used incorrect path `/docs/module-01/intro-physical-ai`
**Solution**: Updated to correct path `/docs/module1/week1-intro-physical-ai` matching actual file structure
**File**: `docs/src/pages/index.tsx`

### 2. Chatbot Source Links
**Problem**: Backend `_source_to_nav_path` function generated paths without GitHub Pages base URL prefix
**Solution**: Added `base_url = "/physical-ai-and-humanoid-robotics"` constant and updated path construction
**File**: `backend/src/services/agent_service.py`

**Before**:
```python
return f"/docs/{module}/{page}"  # Missing base URL
```

**After**:
```python
base_url = "/physical-ai-and-humanoid-robotics"
return f"{base_url}/docs/{module}/{page}"  # Correct full path
```

### 3. Footer Organization Links
**Problem**: Footer linked to Panaversity and PIAIC instead of BasenAI
**Solution**: Updated Community section links to BasenAI GitHub and LinkedIn
**File**: `docs/docusaurus.config.ts`

**Changes**:
- Replaced "Panaversity" → "BasenAI GitHub" (https://github.com/orgs/basenai/dashboard)
- Replaced "PIAIC" → "BasenAI LinkedIn" (https://www.linkedin.com/company/basenai)

### Validation
- Ran `getDiagnostics` on all modified files: ✅ All passed with no errors
- Verified paths match actual file structure in `docs/docs/` directory
- Confirmed regex pattern correctly extracts module and page names

## Outcome

- ✅ Impact: Fixed 3 categories of broken/incorrect links affecting user navigation and trust
- 🧪 Tests: getDiagnostics passed for all 3 modified files
- 📁 Files: 3 files modified (index.tsx, agent_service.py, docusaurus.config.ts)
- 🔁 Next prompts: Manual testing of homepage navigation, chatbot source links, and footer links
- 🧠 Reflection: Minimal, targeted changes reduced risk; hardcoded base URL matches Docusaurus pattern for consistency

## Evaluation notes (flywheel)

- Failure modes observed: None during implementation
- Graders run and results (PASS/FAIL): Diagnostics PASS for all files
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add automated link validation to CI/CD pipeline to catch similar issues earlier
