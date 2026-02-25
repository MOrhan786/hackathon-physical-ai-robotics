# Physical AI & Humanoid Robotics Textbook Constitution

## Core Principles

### I. Content-First Development
Every feature serves the educational mission. The textbook content (13 weeks, 4 modules) is the primary deliverable. Interactive features (chat, personalization, translation) enhance learning but must never compromise content accessibility. The site must work as a readable textbook even if all APIs are offline.

### II. Jamstack Architecture
Frontend is a static site (Docusaurus) deployed to CDN (Vercel). Backend is a decoupled API (HuggingFace Spaces). This separation ensures: zero-cost frontend hosting, independent scaling, content versioned in Git, API can be swapped without frontend changes.

### III. User-Adaptive Learning
Content adapts to each learner's background. At signup, we collect: programming experience (beginner/intermediate/advanced), robotics experience (none/hobbyist/professional), preferred languages (Python/C++/JS/Rust/Java), hardware access (Jetson/RPi/Arduino/RealSense/LIDAR). This data drives personalization and future content recommendations.

### IV. Accessibility & Inclusivity
The textbook must be accessible to users across: language barriers (Urdu translation), experience levels (content personalization), hardware budgets (4-tier hardware guide from $50/mo cloud to $90K+ lab), and device types (mobile-friendly with CORS and responsive design).

### V. Smallest Viable Change
Every code change should be the minimum needed. Prefer editing existing files over creating new ones. No speculative features, no premature abstractions. Three similar lines are better than a premature utility function. YAGNI applies.

### VI. Security by Default
Never hardcode secrets or API keys in source code. Use environment variables and `.env` files. API keys go in `docusaurus.config.ts` customFields via `process.env`. Input validation at all boundaries. CORS explicitly configured.

## Technology Standards

### Stack
- **Frontend**: Docusaurus 3.x, React 19, TypeScript 5.6, CSS Modules
- **Backend**: FastAPI (Python), RAG pipeline, LLM integration
- **Frontend Deploy**: Vercel (static site)
- **Backend Deploy**: HuggingFace Spaces
- **Version Control**: Git + GitHub

### Code Quality
- TypeScript strict mode for type safety
- CSS Modules for scoped styling (no global CSS pollution)
- React hooks only (no class components)
- Default exports for page/layout components
- Named exports for utilities and context
- PascalCase for components, camelCase for functions/variables, UPPER_CASE for constants

### Content Standards
- Every week must include: learning objectives, theory, code examples, assessment questions
- Code examples must be working Python/XML/Bash with proper syntax highlighting
- Use Mermaid diagrams for architecture visualization
- Assessment questions follow Bloom's taxonomy (Recall → Apply → Analyze)

## Development Workflow

### Feature Development
1. Check spec.md for requirements
2. Implement smallest viable change
3. Test manually (verify in browser)
4. Update tasks.md status
5. Create PHR (Prompt History Record) for session

### Deployment
1. `npm run build` — verify no build errors
2. `git push` to main — triggers Vercel auto-deploy
3. Backend changes — deploy to HuggingFace Space
4. Verify live site after deployment

### Content Updates
1. Edit markdown file in `docs/`
2. Preview with `npm start`
3. Verify code examples render correctly
4. Check sidebar navigation works

## Governance

This constitution governs all development on the Physical AI & Humanoid Robotics Textbook project. It was reverse-engineered from existing codebase patterns and ratified for ongoing development. Amendments require documentation and must be reflected in this file.

All changes must comply with these principles. The spec (`specs/physical-ai-textbook/spec.md`) is the authoritative source for feature requirements.

**Version**: 1.0.0 | **Ratified**: 2026-02-19 | **Last Amended**: 2026-02-19
