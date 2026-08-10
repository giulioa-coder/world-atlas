# World Atlas Frontend

Frontend React/Next.js per World Atlas - una piattaforma di cartografia AI per scrittori.

## Requisiti

- Node.js 18+ 
- npm o yarn
- Backend World Atlas in esecuzione su http://localhost:8000

## Installazione

```bash
# Copia il file di esempio delle variabili d'ambiente
cp .env.example .env.local

# Installa le dipendenze
npm install

# Avvia il server di sviluppo
npm run dev
```

L'applicazione sarà disponibile su http://localhost:3000

## Struttura del Progetto

```
frontend/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Home page
│   ├── layout.tsx         # Layout principale
│   └── worlds/            # Pagine dei mondi
├── components/
│   ├── ui/                # Componenti UI riutilizzabili
│   ├── map/               # Componenti della mappa
│   └── manuscript/        # Componenti upload manoscritti
├── stores/                # Zustand stores (gestione stato)
├── lib/                   # Utility e API client
├── types/                 # Tipi TypeScript
└── public/                # Asset statici
```

## Funzionalità

### Home Page
- Lista di tutti i mondi creati
- Creazione nuovo mondo
- Navigazione ai dettagli del mondo

### Mappa Interattiva
- Visualizzazione SVG delle località
- Drag & drop per spostare le località
- Zoom e pan della mappa
- Layer toggle (politico, geografico, strade, etc.)
- Creazione e modifica località

### Upload Manoscritti
- Supporto per TXT, PDF, DOCX
- Validazione tipo e dimensione file
- Feedback visivo durante l'upload
- Integrazione con backend per l'estrazione entità

### Gestione Mondi
- CRUD completo per mondi, località, personaggi
- Timeline dei viaggi dei personaggi
- Wiki automatica del mondo
- Rilevamento incongruenze geografiche

## Variabili d'Ambiente

| Nome | Descrizione | Default |
|------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | URL del backend API | `http://localhost:8000/api/v1` |
| `NEXT_PUBLIC_DEBUG` | Abilita debug mode | `false` |

## Comandi Disponibili

```bash
npm run dev      # Avvia server di sviluppo
npm run build    # Build per produzione
npm run start    # Avvia server produzione
npm run lint     # Esegui linting
```

## Stack Tecnologico

- **React 18** - Libreria UI
- **Next.js 14** - Framework React
- **TypeScript** - Type safety
- **Zustand** - State management
- **Tailwind CSS** - Styling
- **Radix UI** - Componenti accessibili
- **Lucide React** - Icone
- **React Dropzone** - Upload file
- **Axios** - Client HTTP

## Sviluppo

### Aggiungere nuovi componenti

I componenti UI seguono il pattern di shadcn/ui:

```tsx
import { cn } from "@/lib/utils"

export const MyComponent = ({ className, ...props }) => (
  <div className={cn("base-styles", className)} {...props} />
)
```

### Chiamate API

Usa il client API già configurato:

```tsx
import { api } from '@/lib/api'

const worlds = await api.worlds.list()
const location = await api.locations.create(worldId, data)
```

### Gestione Stato

Usa gli store Zustand:

```tsx
import { useWorldStore } from '@/stores/worldStore'

const { worlds, fetchWorlds, createWorld } = useWorldStore()
```

## License

MIT
