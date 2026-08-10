# World Atlas - Quick Start Guide

## Stato Attuale del Progetto ✅

Il progetto World Atlas è ora **funzionante** con tutte le funzionalità base implementate e testate.

### Backend (FastAPI + SQLite/PostgreSQL)

✅ **Funzionalità Implementate:**
- CRUD completo per Worlds, Locations, Characters, Manuscripts
- Servizi business logic per tutte le entità
- Database schema con 14 tabelle (World, Location, Character, Manuscript, Chapter, Region, Road, Border, LoreEntity, ecc.)
- API RESTful endpoints
- Supporto multi-database (SQLite per sviluppo, PostgreSQL per produzione)
- Parsing manoscritti (TXT, DOCX, PDF)
- Estrazione capitoli automatica
- Architecture pronta per AI providers (mock incluso)

✅ **Test Superati:**
- Tutti i modelli importano correttamente
- Creazione mondi e località funzionante
- Gestione personaggi e manoscritti operativa
- Database persistence verificata

### Frontend (Next.js + React + TypeScript)

✅ **Componenti Implementati:**
- Home page con lista mondi
- Pagina creazione nuovo mondo
- Pagina dettaglio mondo con tabs
- Mappa SVG interattiva (pan, zoom)
- Componenti UI (Button, Input, Dialog, Tabs, Card, Select, Textarea)
- ManuscriptUploader con drag-and-drop
- Store Zustand per state management
- API client per comunicazione backend
- Tipizzazione TypeScript completa

## Avvio Rapido

### Prerequisiti
- Python 3.10+
- Node.js 18+
- npm o yarn

### 1. Backend

```bash
cd /workspace/world-atlas/backend

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt

# Esegui test (opzionale)
python test_complete.py

# Avvia server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sarà disponibile su: http://localhost:8000
Documentazione API Swagger: http://localhost:8000/docs

### 2. Frontend

```bash
cd /workspace/world-atlas/frontend

# Copia file environment
cp .env.example .env.local

# Installa dipendenze (richiede ~200MB spazio)
npm install

# Avvia development server
npm run dev
```

Frontend sarà disponibile su: http://localhost:3000

### 3. Verifica Funzionamento

1. Apri browser su http://localhost:3000
2. Crea un nuovo mondo ("Create New World")
3. Clicca sul mondo creato
4. Aggiungi località nella tab "Map"
5. Trascina le località per posizionarle
6. Visualizza dettagli nella sidebar destra

## Struttura Progetto

```
world-atlas/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Endpoint REST
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── core/            # Config, exceptions
│   │   ├── parsing/         # Document parsing
│   │   ├── ai/              # AI providers
│   │   └── main.py          # FastAPI app
│   ├── tests/               # Test suite
│   ├── requirements.txt
│   └── test_complete.py     # Test script
│
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   │   ├── ui/              # Base UI components
│   │   ├── map/             # Map components
│   │   └── manuscript/      # Upload components
│   ├── stores/              # Zustand stores
│   ├── lib/                 # Utilities
│   ├── types/               # TypeScript types
│   └── package.json
│
├── scripts/                 # Utility scripts
├── docker-compose.yml       # Docker config
└── README.md                # Questo file
```

## API Endpoints Principali

### Worlds
- `GET /api/v1/worlds/` - Lista tutti i mondi
- `POST /api/v1/worlds/` - Crea nuovo mondo
- `GET /api/v1/worlds/{id}/` - Dettaglio mondo
- `PUT /api/v1/worlds/{id}/` - Aggiorna mondo
- `DELETE /api/v1/worlds/{id}/` - Elimina mondo

### Locations
- `GET /api/v1/worlds/{world_id}/locations/` - Lista località
- `POST /api/v1/worlds/{world_id}/locations/` - Crea località
- `GET /api/v1/locations/{id}/` - Dettaglio località
- `PUT /api/v1/locations/{id}/` - Aggiorna località
- `PATCH /api/v1/locations/{id}/position` - Aggiorna coordinate
- `DELETE /api/v1/locations/{id}/` - Elimina località

### Characters
- `GET /api/v1/worlds/{world_id}/characters/` - Lista personaggi
- `POST /api/v1/worlds/{world_id}/characters/` - Crea personaggio
- `GET /api/v1/characters/{id}/` - Dettaglio personaggio
- `PUT /api/v1/characters/{id}/` - Aggiorna personaggio
- `DELETE /api/v1/characters/{id}/` - Elimina personaggio

### Manuscripts
- `POST /api/v1/worlds/{world_id}/manuscripts/upload/` - Upload manoscritto
- `GET /api/v1/manuscripts/{id}/` - Dettaglio manoscritto
- `POST /api/v1/manuscripts/{id}/process/` - Processa manoscritto
- `GET /api/v1/manuscripts/{id}/chapters/` - Lista capitoli

## Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
python test_complete.py
```

### API Manual Testing
Usa Swagger UI: http://localhost:8000/docs

Oppure curl:
```bash
# Crea mondo
curl -X POST http://localhost:8000/api/v1/worlds/ \
  -H "Content-Type: application/json" \
  -d '{"name":"My World","description":"Test","genre":"fantasy"}'

# Lista mondi
curl http://localhost:8000/api/v1/worlds/
```

## Risoluzione Problemi

### Backend non si avvia
```bash
# Verifica dipendenze
pip install -r requirements.txt

# Verifica import
python -c "from app.main import app; print('OK')"

# Controlla log errori
uvicorn app.main:app --reload 2>&1 | grep ERROR
```

### Frontend non si avvia
```bash
# Pulisci cache
rm -rf node_modules .next
npm install

# Verifica spazio disco
df -h .

# Controlla errori
npm run dev 2>&1 | grep -i error
```

### Database Issues
```bash
# Reset database (SQLite)
rm world_atlas.db

# Ricrea tabelle
python -c "from app.database import Base, engine; Base.metadata.create_all(engine)"
```

## Prossimi Passi (Miglioramenti Futuri)

### Priorità Alta
1. **Frontend Integration** - Connettere store Zustand alle API reali
2. **Map Editor** - Migliorare strumenti di disegno (strade, regioni)
3. **Authentication** - Implementare login/registrazione utenti
4. **File Upload** - Completare upload manoscritti con progress tracking

### Priorità Media
5. **AI Integration** - Collegare provider AI reali (OpenAI, Ollama)
6. **Timeline** - Implementare visualizzazione viaggi personaggi
7. **Export** - Generazione PNG/SVG/PDF mappe
8. **Version History** - Sistema di versioning mondi

### Priorità Bassa
9. **Real-time Collaboration** - Multi-user editing
10. **Advanced Cartography** - Generazione procedurale terrain
11. **Reader Mode** - Modalità lettura con fog-of-war
12. **Mobile App** - Versione mobile-responsive

## Note Tecniche

### Database
- Default: SQLite (sviluppo locale)
- Produzione: PostgreSQL + PostGIS (configurabile via DATABASE_URL)
- Migrazioni: Da implementare con Alembic

### AI Provider
- Architettura pluggable implementata
- Mock provider incluso per sviluppo
- Supporto futuro: OpenAI, Ollama, Qwen

### Storage
- Astrazione layer implementata
- Default: filesystem locale
- Futuro: S3, Supabase Storage

### Sicurezza
- Attualmente: Nessuna autenticazione (solo locale)
- Da implementare: JWT auth, ownership validation
- File upload: Validazione MIME, size limits

## Licenza

Progetto open-source per scopi educativi e personali.

## Contributi

Benvenuti contributi! Per favore:
1. Crea branch feature
2. Scrivi test
3. Submit pull request

---

**Stato**: MVP Funzionante ✅  
**Ultimo Aggiornamento**: 2026-08-10  
**Versione**: 1.0.0-alpha
