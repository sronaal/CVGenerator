# CV Generator - ATS Optimized Resume Builder

AI-powered SaaS application that generates ATS-optimized CVs using Microsoft Word templates.

## Stack

- **Frontend**: Next.js 14 + TypeScript + TailwindCSS
- **Backend**: FastAPI (Python) + SQLAlchemy + PostgreSQL
- **AI**: Ollama (default) or Gemini Flash Lite
- **Cache**: Redis
- **DOCX**: python-docx

## Quick Start

### 1. Start Infrastructure

```bash
docker-compose up -d
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. AI Provider

**Ollama (default):**
```bash
ollama pull llama3.1
ollama serve
```

**Gemini:**
Edit `.env`:
```
AI_PROVIDER=gemini
GEMINI_API_KEY=your-key
GEMINI_MODEL=gemini-2.0-flash-lite
```

## Architecture

```
User → Next.js Frontend
  ↓
FastAPI Backend
  ├── Auth (JWT)
  ├── Profile Engine
  ├── Job Offer Parser (AI)
  ├── ATS Matching Engine
  ├── Resume Optimizer (AI)
  └── DOCX Generator (python-docx)
```

## API Endpoints

- `POST /api/v1/auth/register` - Register
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/profiles/me` - Get profile
- `POST /api/v1/profiles/me/experiences` - Add experience
- `POST /api/v1/profiles/me/projects` - Add project
- `POST /api/v1/job-offers/parse` - Parse job offer with AI
- `POST /api/v1/matching/analyze` - ATS match analysis
- `POST /api/v1/generate` - Generate optimized CV (.docx)
