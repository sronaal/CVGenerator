# CV Generator — Generador de CV Optimizados para ATS

App SaaS que genera CVs optimizados para Applicant Tracking Systems (ATS) usando plantillas Microsoft Word e IA.

## Stack

| Componente | Tecnología |
|---|---|
| **Frontend** | Next.js 14 + TypeScript + TailwindCSS |
| **Backend** | FastAPI + SQLAlchemy 2.0 + PostgreSQL |
| **AI** | Gemini 2.0 Flash Lite (default) · Ollama (alternativa) |
| **Cache** | Redis (AI responses + idempotencia) |
| **DOCX** | python-docx (plantilla Harvard `2025-template_bullet.docx`) |

## Quick Start

### 1. Infraestructura (PostgreSQL + Redis)

```bash
docker compose up -d
```

Verificar:
```bash
docker ps
# cvgen_postgres (5432) y cvgen_redis (6379) deben estar running
```

### 2. Backend

```bash
cd backend
source venv/bin/activate

# Solo primera vez: migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: `http://localhost:8000/docs`

### 3. Frontend

```bash
cd frontend
pnpm install   # solo primera vez
pnpm dev
```

Frontend: `http://localhost:3000`

### 4. AI Provider

**Gemini (default):** Editar `backend/.env`:
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=tu-api-key-de-google-ai-studio
```

Conseguir API key gratis: https://aistudio.google.com/apikey

**Ollama (alternativa):**
```bash
ollama pull llama3.1
ollama serve
```
```env
AI_PROVIDER=ollama
```

### 5. Limpiar cache (si es necesario)

```bash
docker exec cvgen_redis redis-cli FLUSHALL
```

## Variables de Entorno

### `backend/.env`

```env
# Base de datos
DATABASE_URL=postgresql+asyncpg://cvgen:cvgen_secret@localhost:5432/cvgen_db

# Cache (Redis)
REDIS_URL=redis://localhost:6379/0

# Auth (JWT)
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI — Gemini (default)
AI_PROVIDER=gemini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.0-flash-lite
GEMINI_MAX_TOKENS=2048

# AI — Ollama (alternativa)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Cache TTL para respuestas AI (24h en segundos)
AI_CACHE_TTL=86400

# General
LOG_LEVEL=INFO
APP_ENV=development
```

### `frontend/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Idempotencia y Cache

Todas las llamadas a la API de Gemini se cachean en Redis para evitar consumo excesivo de tokens:

| Endpoint | Cache key | TTL | Comportamiento idempotente |
|---|---|---|---|
| `POST /job-offers/parse` | `ai:parse:{sha256(raw_text)}` | 24h | Misma `raw_text` → mismo `JobOffer` |
| `POST /generate` | `ai:prompt:{sha256(prompt)}` | 7d | Mismo (profile, job_offer) → mismo `GeneratedCV` |
| `chat()` interno | `ai:prompt:{sha256(prompt)}` | 7d | Mismo prompt → misma respuesta |

Si Redis no está disponible, el sistema funciona sin cache (graceful degradation).

## Arquitectura

```
User → Next.js (Frontend :3000)
                ↓ API REST
         FastAPI (Backend :8000)
                ↓
  ┌─────────────────────────────┐
  │ Auth (JWT) · Profile CRUD   │
  │ Job Offer Parser (Gemini)   │ ← Redis Cache
  │ ATS Matcher (rule-based)    │
  │ Resume Optimizer (Gemini)   │ ← Redis Cache
  │ DOCX Generator (template)   │
  └─────────────────────────────┘
                ↓
         PostgreSQL · Redis
```

El **ATS Matcher** es 100% rule-based (normalización de skills + scoring matemático). **No consume tokens AI**.

## API Endpoints

### Auth
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/auth/register` | Registrar usuario |
| POST | `/api/v1/auth/login` | Login (JWT) |
| GET | `/api/v1/auth/me` | Usuario actual |

### Profile
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/profiles/me` | Perfil completo con relaciones |
| PUT | `/api/v1/profiles/me` | Actualizar perfil |

### Experiencias
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/profiles/me/experiences` | Crear |
| GET | `/api/v1/profiles/me/experiences` | Listar |
| PUT | `/api/v1/profiles/me/experiences/{id}` | Actualizar |
| DELETE | `/api/v1/profiles/me/experiences/{id}` | Eliminar |

### Educación
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/profiles/me/education` | Crear |
| GET | `/api/v1/profiles/me/education` | Listar |
| PUT | `/api/v1/profiles/me/education/{id}` | Actualizar |
| DELETE | `/api/v1/profiles/me/education/{id}` | Eliminar |

### Skills
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/profiles/me/skills` | Crear |
| GET | `/api/v1/profiles/me/skills` | Listar |
| PUT | `/api/v1/profiles/me/skills/{id}` | Actualizar |
| DELETE | `/api/v1/profiles/me/skills/{id}` | Eliminar |

### Certificaciones
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/profiles/me/certifications` | Crear |
| GET | `/api/v1/profiles/me/certifications` | Listar |
| PUT | `/api/v1/profiles/me/certifications/{id}` | Actualizar |
| DELETE | `/api/v1/profiles/me/certifications/{id}` | Eliminar |

### Proyectos
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/profiles/me/projects` | Crear |
| GET | `/api/v1/profiles/me/projects` | Listar |
| PUT | `/api/v1/profiles/me/projects/{id}` | Actualizar |
| DELETE | `/api/v1/profiles/me/projects/{id}` | Eliminar |

### Idiomas
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/profiles/me/languages` | Crear |
| GET | `/api/v1/profiles/me/languages` | Listar |
| PUT | `/api/v1/profiles/me/languages/{id}` | Actualizar |
| DELETE | `/api/v1/profiles/me/languages/{id}` | Eliminar |

### Job Offers
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/job-offers/parse` | Parsear oferta con Gemini |
| GET | `/api/v1/job-offers` | Listar |
| GET | `/api/v1/job-offers/{id}` | Obtener |
| DELETE | `/api/v1/job-offers/{id}` | Eliminar |

### Matching
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/matching/analyze` | Análisis ATS (rule-based) |

### Generate
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/generate` | Generar CV optimizado (.docx) |
| GET | `/api/v1/generate/{id}/download` | Descargar CV (requiere JWT) |
| GET | `/api/v1/generate/history` | Historial de CVs generados |

### Auth — Recuperación de Contraseña

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/v1/auth/forgot-password` | Solicitar reset (token por email/log) |
| POST | `/api/v1/auth/reset-password` | Cambiar contraseña con token |

## Troubleshooting

### Error: "Not authenticated" al descargar CV
La descarga usa `fetch` con JWT. Si ves este error, el token expiró o no está en localStorage. Re-loguéate.

### Error: "No module named 'app'"
Ejecuta uvicorn desde el directorio `backend/`:
```bash
cd backend && uvicorn app.main:app --reload
```

### Error: "400 Email already registered"
El email ya existe. Usa otro o haz login.

### Error: Redis connection refused
Redis no está corriendo. Inicia con `docker compose up -d`.

### Error: Gemini devuelve parsed_json vacío
Verifica que `GEMINI_API_KEY` esté configurada en `backend/.env`. Limpia cache:
```bash
docker exec cvgen_redis redis-cli FLUSHALL
```

### El CV se genera pero no muestra datos de secciones
Completa la sección correspondiente desde el dashboard (profile → sección). Las secciones sin datos se omiten del CV.

## Comandos Rápidos

```bash
# Backend
cd backend && source venv/bin/activate
alembic upgrade head                 # aplicar migraciones
alembic revision --autogenerate -m "desc"  # crear migración
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend && pnpm dev

# Infra
docker compose up -d                 # iniciar servicios
docker compose down                  # detener
docker compose down -v               # detener y borrar datos
docker exec cvgen_redis redis-cli FLUSHALL  # limpiar cache
```
