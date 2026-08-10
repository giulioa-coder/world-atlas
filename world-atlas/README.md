# World Atlas - AI Cartography Platform for Writers

A production-quality web application that transforms manuscripts into structured, editable, interactive world maps.

## Core Principle

> **MANUSCRIPT → NARRATIVE EXTRACTION → STRUCTURED WORLD MODEL → GEOGRAPHICAL CONSISTENCY → CARTOGRAPHIC RENDERING → INTERACTIVE MAP**

The generated map is **editable and reproducible**. The application never depends exclusively on a single generated raster image.

## Architecture

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Zustand
- **Backend**: FastAPI, Python 3.11+, Pydantic v2, SQLAlchemy 2.0
- **Database**: PostgreSQL 15+ with PostGIS
- **Map Rendering**: SVG-based with Canvas optimization

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Development Setup

```bash
# Start database and Redis
docker-compose up -d postgres redis

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Visit `http://localhost:3000` for the frontend and `http://localhost:8000/docs` for API docs.

## Project Structure

```
/world-atlas
├── /backend          # FastAPI application
│   ├── /app
│   │   ├── /api      # REST API routes
│   │   ├── /core     # Configuration, security
│   │   ├── /models   # SQLAlchemy ORM models
│   │   ├── /schemas  # Pydantic schemas
│   │   ├── /services # Business logic
│   │   ├── /parsing  # Document parsing
│   │   ├── /ai       # AI provider abstraction
│   │   ├── /cartography # Map generation
│   │   └── /storage  # File storage abstraction
│   └── /tests
│
├── /frontend         # Next.js application
│   ├── /app          # App Router pages
│   ├── /components   # React components
│   ├── /features     # Feature modules
│   ├── /hooks        # Custom hooks
│   ├── /stores       # Zustand state management
│   └── /types        # TypeScript types
│
├── /shared           # Shared types and schemas
├── /docs             # Documentation
└── /scripts          # Development scripts
```

## Features (Phase 1 - MVP)

✅ Manual world creation
✅ Interactive map editor (drag, create, edit, delete locations)
✅ Road drawing between locations
✅ Layer system (political, geographical, roads, settlements)
✅ Multiple map styles
✅ Demo world "Elarion" with sample data
✅ Persistent storage in PostgreSQL
✅ Responsive UI

## Roadmap

- **Phase 2**: Manuscript import (TXT, DOCX, PDF)
- **Phase 3**: AI entity extraction
- **Phase 4**: Constraint-based map generation
- **Phase 5**: Character timeline
- **Phase 6**: Consistency engine
- **Phase 7**: World wiki
- **Phase 8**: Anti-spoiler reader mode
- **Phase 9**: Advanced exports (SVG, PDF)

## Demo World: Elarion

The MVP includes a pre-populated fantasy world with:

**Locations:**
- Aurelia (Capital city)
- Black Forest
- Iron Mountains
- River Serath
- Castle Veyr
- Port Neris
- Village Elden

**Characters:**
- Kael
- Mira
- Toren

Use this demo to test all features immediately.

## Key Architectural Principles

1. **WorldModel is Source of Truth** - All geographical data stored structurally
2. **Renderer is Visual Only** - Maps are rendered from data, not the reverse
3. **Evidence Tracking** - Every AI-extracted fact links to source text
4. **Pluggable AI** - Support multiple AI providers via abstraction
5. **Manual-First** - Works without AI, manual editing always available
6. **Confidence Scoring** - Track certainty of inferred facts
7. **Canonical Status** - Distinguish between author-approved and suggested data

## License

MIT

## Contributing

See [docs/development.md](docs/development.md) for contribution guidelines.
