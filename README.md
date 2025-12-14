# Physical AI & Humanoid Robotics

An interactive educational platform for learning Physical AI and Humanoid Robotics, featuring a Docusaurus-based textbook with an integrated RAG-powered AI chatbot.

## Overview

This project bridges the gap between digital AI and physical robotics, teaching students to design, simulate, and deploy humanoid robots using ROS 2, Gazebo, and NVIDIA Isaac. The platform includes:

- **Interactive Textbook**: Docusaurus-powered documentation with the 5-Step Concept Loop pedagogy
- **RAG Chatbot**: AI assistant that answers questions based on textbook content
- **Personalization**: User authentication, progress tracking, and content translation

## Project Structure

```
├── physical-ai-textbook/     # Docusaurus frontend
│   ├── docs/                 # Course content (MDX)
│   │   ├── module-01/        # ROS 2 Fundamentals
│   │   ├── module2/          # Gazebo & Unity Simulation
│   │   ├── module3/          # NVIDIA Isaac Platform
│   │   └── module4/          # Vision-Language-Action
│   └── src/
│       ├── components/       # React components (Chat, Auth)
│       └── theme/            # Custom Docusaurus theme
├── rag_chatbot/              # FastAPI backend
│   └── src/
│       ├── api/              # REST endpoints
│       ├── services/         # Business logic
│       └── models/           # Data models
├── specs/                    # Feature specifications
├── history/
│   ├── adr/                  # Architecture Decision Records
│   └── prompts/              # Implementation prompts
└── .claude/                  # Claude Code configuration
    ├── agents/               # Specialized AI agents
    ├── skills/               # Agent skill definitions
    └── commands/             # Custom commands
```

## Course Modules

| Module | Topic | Focus |
|--------|-------|-------|
| 1 | ROS 2 Fundamentals | Nodes, Topics, Services, URDF |
| 2 | Gazebo & Unity | Physics simulation, Digital twins |
| 3 | NVIDIA Isaac | Perception, VSLAM, Navigation |
| 4 | Vision-Language-Action | LLM integration, Conversational robotics |

## Tech Stack

**Frontend (Docusaurus)**
- React 18 + TypeScript
- Docusaurus 3.x
- MDX for interactive content
- Custom theme with dark mode

**Backend (RAG Chatbot)**
- FastAPI + Python 3.12
- Qdrant vector database
- Google Gemini API (embeddings + chat)
- Neon Postgres (chat history)

## Quick Start

### Frontend (Textbook)

```bash
cd physical-ai-textbook
npm install
npm run start
```

Access at `http://localhost:3000`

### Backend (RAG Chatbot)

```bash
cd rag_chatbot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run server
python run.py
```

Access API at `http://localhost:8000/docs`

### Ingest Textbook Content

```bash
curl -X POST http://localhost:8000/ingest -H "X-API-Key: your-api-key"
```

## Environment Variables

### Backend (.env)
```ini
GEMINI_API_KEY=your-gemini-key
QDRANT_URL=https://your-qdrant-url
QDRANT_API_KEY=your-qdrant-key
NEON_DB_URL=postgres://...
API_KEY=your-secure-api-key
```

### Frontend (.env)
```ini
REACT_APP_API_URL=http://localhost:8000
```

## Feature Specifications

| Spec | Feature | Status |
|------|---------|--------|
| 001 | RAG Chat UI Integration (Initial) | Completed |
| 002 | RAG Chat UI Integration (Full) | Completed |
| 002 | RAG Chatbot Backend | Completed |
| 003 | Gemini API Migration | Completed |
| 004 | RAG Vector Retrieval Fix | Completed |
| 005 | Website Redesign & UI | Completed |

## Hardware Requirements

For full course experience with simulation:

**Workstation**
- GPU: NVIDIA RTX 4070 Ti+ (12GB VRAM)
- CPU: Intel i7 13th Gen+ / AMD Ryzen 9
- RAM: 64GB DDR5
- OS: Ubuntu 22.04 LTS

**Edge Kit (Optional)**
- NVIDIA Jetson Orin Nano (8GB)
- Intel RealSense D435i
- ReSpeaker USB Mic Array

## Development

### Claude Code Agents

The project includes specialized AI agents:
- `physical-ai-author`: Textbook content generation
- `fastapi-specialist`: Backend development
- `react-frontend-specialist`: UI components
- `rag-backend-engineer`: RAG pipeline
- `docusaurus-architect-specialist`: Site architecture

### Custom Commands

```bash
# Generate spec
/sp.specify

# Create implementation plan
/sp.plan

# Generate ADR
/sp.adr
```

## License

MIT

## Contributing

1. Create a feature spec in `specs/`
2. Implement following the spec
3. Document decisions in `history/adr/`
4. Submit PR with linked spec
