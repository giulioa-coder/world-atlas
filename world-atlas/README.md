# World Atlas 🌍

Piattaforma di cartografia AI per scrittori - Trasforma il tuo manoscritto in una mappa del mondo interattiva.

## Panoramica

World Atlas è uno strumento professionale per autori che permette di:

- **Caricare manoscritti** (TXT, PDF, DOCX) ed estrarre automaticamente località geografiche
- **Generare mappe del mondo** basate sulle informazioni estratte dal testo
- **Modificare manualmente** la mappa con un editor cartografico completo
- **Creare timeline** dei viaggi dei personaggi
- **Rilevare incongruenze** geografiche e temporali nella narrazione
- **Generare wiki automatiche** del mondo creato
- **Esportare mappe** in PNG, SVG e PDF ad alta risoluzione

## Architettura

```
world-atlas/
├── backend/           # FastAPI + PostgreSQL
│   ├── app/
│   │   ├── api/       # Endpoint REST
│   │   ├── models/    # Modelli SQLAlchemy
│   │   ├── schemas/   # Schemi Pydantic
│   │   ├── services/  # Business logic
│   │   └── parsing/   # Parser documenti
│   └── tests/
├── frontend/          # Next.js + React + TypeScript
│   ├── app/           # App Router
│   ├── components/    # Componenti UI
│   ├── stores/        # Zustand state management
│   └── lib/           # API client & utilities
└── scripts/           # Script di utilità
```

## Quick Start

### Prerequisiti

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+ (con PostGIS opzionale)
- Docker (opzionale, per deployment)

### Backend

```bash
cd backend

# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o .\venv\Scripts\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt

# Configura ambiente
cp .env.example .env
# Modifica .env con le tue impostazioni DB

# Avvia server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Il backend sarà disponibile su http://localhost:8000

### Frontend

```bash
cd frontend

# Copia variabili d'ambiente
cp .env.example .env.local

# Installa dipendenze
npm install

# Avvia server di sviluppo
npm run dev
```

Il frontend sarà disponibile su http://localhost:3000

## Funzionalità Principali

### 1. Importazione Manoscritti
- Supporto per TXT, PDF, DOCX
- Rilevamento automatico capitoli
- Estrazione entità con AI (opzionale)
- Tracking evidenze testuali

### 2. Mappa Interattiva
- Rendering SVG di alta qualità
- Drag & drop località
- Layer multipli (politico, geografico, strade, etc.)
- Stili cartografici intercambiabili
- Zoom, pan, ricerca

### 3. Timeline Viaggi
- Tracciamento percorsi personaggi
- Animazione cronologica
- Calcolo tempi di viaggio
- Rilevamento incongruenze

### 4. World Wiki
- Enciclopedia automatica del mondo
- Link incrociati tra entità
- Generazione articoli da testo

### 5. Reader Mode
- Fog-of-war basato sui capitoli
- Protezione spoiler
- Modalità lettore interattiva

### 6. Export
- PNG (configurabile DPI)
- SVG vettoriale
- PDF print-ready
- Selezione layer visibili

## Stack Tecnologico

### Backend
- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database (con supporto PostGIS)
- **Pydantic** - Validazione dati
- **python-docx, PyPDF2** - Parsing documenti

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Type safety
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **Radix UI** - Componenti accessibili
- **React Dropzone** - Upload file

## Demo World

Il progetto include un mondo demo "Elarion" pre-configurato con:
- 11 località (città, foreste, montagne, fiumi)
- Personaggi esempio
- Capitoli demo per testare l'estrazione

Per caricarlo:
```bash
cd backend
source venv/bin/activate
python scripts/seed_demo.py
```

## API Endpoints

### Worlds
- `GET /api/v1/worlds` - Lista mondi
- `POST /api/v1/worlds` - Crea mondo
- `GET /api/v1/worlds/{id}` - Dettaglio mondo
- `PUT /api/v1/worlds/{id}` - Aggiorna mondo
- `DELETE /api/v1/worlds/{id}` - Elimina mondo

### Locations
- `GET /api/v1/worlds/{id}/locations` - Lista località
- `POST /api/v1/worlds/{id}/locations` - Crea località
- `PUT /api/v1/worlds/{id}/locations/{loc_id}` - Aggiorna località
- `DELETE /api/v1/worlds/{id}/locations/{loc_id}` - Elimina località

### Manuscripts
- `GET /api/v1/worlds/{id}/manuscripts` - Lista manoscritti
- `POST /api/v1/worlds/{id}/manuscripts` - Upload manoscritto
- `GET /api/v1/manuscripts/{id}/chapters` - Lista capitoli

### Characters
- `GET /api/v1/worlds/{id}/characters` - Lista personaggi
- `POST /api/v1/worlds/{id}/characters` - Crea personaggio

## Configurazione

### Variabili d'Ambiente Backend

```env
DATABASE_URL=postgresql://user:password@localhost/world_atlas
SECRET_KEY=your-secret-key-min-32-chars
DEBUG=true
MAX_FILE_SIZE_MB=50
```

### Variabili d'Ambiente Frontend

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_DEBUG=false
```

## Sviluppo

### Eseguire Test Backend

```bash
cd backend
pytest
```

### Build Frontend Produzione

```bash
cd frontend
npm run build
npm run start
```

## Roadmap

- [ ] Autenticazione utenti
- [ ] Migrazioni Alembic
- [ ] Test automatizzati completi
- [ ] Integrazione AI provider reali (OpenAI, Qwen, Ollama)
- [ ] Motore constraint geografico avanzato
- [ ] Collaborazione real-time
- [ ] Version history mondi
- [ ] Export EPUB interattivo

## Contributing

1. Fork il repository
2. Crea branch feature (`git checkout -b feature/amazing-feature`)
3. Commit cambiamenti (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Apri Pull Request

## License

MIT License - vedi LICENSE per dettagli

## Supporto

Per problemi, domande o suggerimenti, apri una issue su GitHub.

---

**Nota**: Questo è un progetto in sviluppo attivo. Alcune funzionalità potrebbero essere incomplete o in fase di testing.
