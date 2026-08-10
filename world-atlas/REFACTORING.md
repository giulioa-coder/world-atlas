# World Atlas - Ristrutturazione del Codice

Questo documento descrive le migliorie apportate all'architettura del codice per seguire le best practice.

## Backend (FastAPI/Python)

### Nuova Struttura

```
backend/app/
├── api/                    # API routers (unchanged)
├── core/                   # Configurazione ed eccezioni (unchanged)
├── database.py             # Configurazione DB (unchanged)
├── main.py                 # Application entry point (unchanged)
├── middleware/             # [NUOVO] Middleware personalizzati
├── models/                 # SQLAlchemy models (unchanged)
├── repositories/           # [NUOVO] Repository pattern
│   ├── __init__.py
│   ├── base.py            # Repository base generico
│   ├── world_repository.py
│   ├── location_repository.py
│   ├── manuscript_repository.py
│   └── character_repository.py
├── schemas/                # Pydantic schemas (unchanged)
├── services/               # Business logic (refactored)
│   ├── world_service.py
│   ├── location_service.py
│   ├── manuscript_service.py
│   └── character_service.py
├── parsing/                # Manuscript parsing (unchanged)
└── storage/                # File storage (unchanged)
```

### Miglioramenti Implementati

#### 1. Repository Pattern
- **Base Repository**: Classe generica con operazioni CRUD di base
- **Repository Specifici**: Ogni entità ha il proprio repository con metodi specializzati
- **Vantaggi**:
  - Separazione chiara tra logica di accesso ai dati e business logic
  - Maggiore testabilità
  - Codice DRY (Don't Repeat Yourself)

#### 2. Service Layer Refactoring
- I servizi ora utilizzano i repository invece di accedere direttamente al DB
- Metodi più concisi e focalizzati sulla business logic
- Esempio `WorldService`:
  ```python
  class WorldService:
      def __init__(self, db: Session):
          self.db = db
          self.repository = WorldRepository(db)
      
      def create(self, schema: WorldCreate, is_demo: bool = False) -> World:
          return self.repository.create(
              name=schema.name,
              description=schema.description,
              genre=schema.genre,
              visual_style=schema.visual_style,
              scale_km_per_unit=schema.scale_km_per_unit,
              is_demo=is_demo,
          )
  ```

#### 3. Exception Handling
- Sistema di eccezioni già presente in `app/core/exceptions.py`
- Pronto per essere integrato con exception handlers globali

### Prossimi Passi Consigliati

1. **Dependency Injection**: Implementare Depends() avanzato per servizi e repository
2. **Exception Handlers**: Aggiungere handler globali in main.py
3. **Unit Tests**: Testare repository e servizi separatamente
4. **Async Support**: Valutare migrazione a SQLAlchemy async

---

## Frontend (Next.js/TypeScript)

### Nuova Struttura

```
frontend/
├── app/                    # Next.js App Router (unchanged)
├── components/             # React components (unchanged)
├── hooks/                  # [NUOVO] Custom React hooks
├── lib/                    # [NUOVO] Utility e configurazione
│   └── api-client.ts      # Client API configurabile
├── services/               # [NUOVO] API services
│   ├── index.ts
│   ├── worldService.ts
│   ├── locationService.ts
│   ├── manuscriptService.ts
│   └── characterService.ts
├── stores/                 # Zustand stores (refactored)
│   ├── worldStore.ts
│   └── mapStore.ts
├── styles/                 # CSS/Tailwind (unchanged)
├── types/                  # TypeScript types (unchanged)
└── package.json
```

### Miglioramenti Implementati

#### 1. API Client Centralizzato
- **File**: `lib/api-client.ts`
- **Features**:
  - Gestione centralizzata degli errori
  - Tipizzazione delle risposte
  - Configurazione della base URL
  - Classe `ApiClientError` personalizzata

```typescript
export async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, config);
  return handleResponse<T>(response);
}
```

#### 2. Service Layer per API
- **Servizi**: `worldService`, `locationService`, `manuscriptService`, `characterService`
- **Vantaggi**:
  - Astrazione delle chiamate API
  - Interfacce tipizzate per input/output
  - Facile da testare e mockare
  - Documentazione inline dei metodi

```typescript
export const worldService = {
  list: async (skip = 0, limit = 100): Promise<PaginatedResponse<World>> => {
    return request<PaginatedResponse<World>>(`/api/v1/worlds/?skip=${skip}&limit=${limit}`);
  },
  
  create: async (data: WorldCreateInput): Promise<World> => {
    return request<World>('/api/v1/worlds/', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  // ... altri metodi
};
```

#### 3. Store Refactoring
- **File**: `stores/worldStore.ts`
- **Miglioramenti**:
  - Utilizzo dei nuovi service layer invece di chiamate API dirette
  - Commenti organizzati per sezione (Worlds, Locations, Manuscripts, Characters)
  - Gestione coerente degli errori
  - Tipizzazione migliorata

```typescript
import { worldService, locationService, manuscriptService, characterService } from '@/services';

// Prima: api.worlds.list()
// Dopo: worldService.list()
```

### Prossimi Passi Consigliati

1. **Custom Hooks**: Creare hook React per operazioni comuni
   ```typescript
   // hooks/useWorlds.ts
   export function useWorlds() {
     const { worlds, fetchWorlds, isLoading, error } = useWorldStore();
     useEffect(() => { fetchWorlds(); }, []);
     return { worlds, isLoading, error };
   }
   ```

2. **React Query**: Valutare TanStack Query per caching e sincronizzazione
3. **Component Library**: Espandere i componenti UI riutilizzabili
4. **Form Validation**: Integrare Zod o Yup per validazione form
5. **Error Boundaries**: Aggiungere error boundaries per gestione errori UI

---

## Vantaggi della Ristrutturazione

### Backend
- ✅ **Separation of Concerns**: Repository (dati) vs Services (business logic)
- ✅ **Testability**: Ogni layer può essere testato indipendentemente
- ✅ **Maintainability**: Codice più organizzato e facile da navigare
- ✅ **Scalability**: Pattern pronti per crescita dell'applicazione

### Frontend
- ✅ **Type Safety**: Tipizzazione completa dalle API agli store
- ✅ **Reusability**: Servizi API riutilizzabili in diversi contesti
- ✅ **Maintainability**: Modifiche alle API richiedono aggiornamenti minimi
- ✅ **Developer Experience**: IntelliSense e autocompletamento migliori

---

## Come Utilizzare la Nuova Struttura

### Backend - Aggiungere una Nuova Entità

1. Creare il Model in `app/models/`
2. Creare lo Schema in `app/schemas/`
3. Creare il Repository in `app/repositories/`
4. Creare/Aggiornare il Service in `app/services/`
5. Creare il Router API in `app/api/v1/`

### Frontend - Chiamare una API

```typescript
// Nei componenti o store
import { worldService } from '@/services';

try {
  const worlds = await worldService.list();
  // Oppure con parametri
  const filtered = await worldService.list(0, 50);
} catch (error) {
  // Gestito automaticamente dal servizio
}
```

---

## Testing

### Backend Test Example
```python
def test_world_repository():
    db = TestingSessionLocal()
    repo = WorldRepository(db)
    
    world = repo.create(name="Test World")
    assert world.name == "Test World"
    
    retrieved = repo.get(world.id)
    assert retrieved.id == world.id
```

### Frontend Test Example
```typescript
// Mock del servizio
jest.mock('@/services', () => ({
  worldService: {
    list: jest.fn().mockResolvedValue({ items: [], total: 0 }),
  },
}));

// Test dello store o componente
```

---

## Conclusioni

La ristrutturazione mantiene la funzionalità esistente mentre introduce pattern architetturali solidi che faciliteranno:
- L'aggiunta di nuove feature
- Il testing automatizzato
- La manutenzione a lungo termine
- L'onboarding di nuovi sviluppatori

Tutti i cambiamenti sono backward-compatible con il codice esistente.
