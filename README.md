# 🐇 Sales Insight Automator — Rabbitt AI

> **Frontend App**: [https://frontend-ten-lovat-84.vercel.app](https://frontend-ten-lovat-84.vercel.app)
> **Backend API**: [https://backend-xi-six-58.vercel.app](https://backend-xi-six-58.vercel.app)
> **Swagger API Docs**: [https://backend-xi-six-58.vercel.app/docs](https://backend-xi-six-58.vercel.app/docs)
> **GitHub Source**: [https://github.com/vidhiverma23/Sales-Insight-Automator](https://github.com/vidhiverma23/Sales-Insight-Automator)

A secure, containerized full-stack application that transforms raw sales data (CSV/XLSX) into professional AI-generated summaries and delivers them via email.

![Architecture](https://img.shields.io/badge/Architecture-FastAPI%20%2B%20React-blueviolet?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-blue?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker)
---

## 🏗️ Architecture Overview

```
┌─────────────────┐     ┌──────────────────────────────────┐
│   React SPA     │────▶│  FastAPI Backend                  │
│   (Vite)        │     │  ├─ POST /api/upload              │
│   Port 3000     │◀────│  ├─ Parser (pandas)               │
└─────────────────┘     │  ├─ AI Engine (Gemini)            │
                        │  ├─ Mailer (Resend)               │
                        │  └─ Swagger: /docs                │
                        │  Port 8000                        │
                        └──────────────────────────────────┘
```

## 🚀 Quick Start with Docker Compose

### Prerequisites
- Docker & Docker Compose installed
- API keys (see below)

### 1. Clone & Configure

```bash
git clone https://github.com/your-username/sales-insight-automator.git
cd sales-insight-automator

# Copy and fill in your API keys
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your keys:
```env
GEMINI_API_KEY=your_gemini_api_key_here
RESEND_API_KEY=your_resend_api_key_here
```

### 2. Launch

```bash
docker-compose up --build
```

### 3. Access

| Service | URL |
|---------|-----|
| 🖥️ Frontend | [http://localhost:3000](http://localhost:3000) |
| 📡 API | [http://localhost:8000](http://localhost:8000) |
| 📖 Swagger Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 📋 ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 🔧 Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Fill in your API keys
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

---

## 🔒 Security Measures

| Layer | Implementation | Details |
|-------|---------------|---------|
| **Rate Limiting** | `slowapi` | 5 requests/minute per IP address |
| **CORS** | FastAPI middleware | Restricted to frontend origin only |
| **Input Validation** | Pydantic + manual | File type (.csv/.xlsx), size (≤10MB), email format |
| **API Key Auth** | `X-API-Key` header | Optional — enable by setting `API_KEY` in `.env` |
| **Security Headers** | Custom middleware | `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy` |
| **File Handling** | In-memory only | Files are never written to disk — processed entirely in memory |
| **Non-root Container** | Dockerfile | Backend runs as `appuser`, not root |

---

## 🤖 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/ci.yml`) triggers on:
- **Pull Requests** to `main`
- **Pushes** to `main`

### Pipeline Steps

| Job | Actions |
|-----|---------|
| **Backend** | Install deps → Lint (Ruff) → Validate imports |
| **Frontend** | Install deps → Lint (ESLint) → Build |
| **Docker** | Build backend image → Build frontend image |

---

## 🌐 Deployment

### Backend → Render

1. Create a new **Web Service** on [Render](https://render.com)
2. Connect your GitHub repo
3. Set:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.example`

### Frontend → Vercel

1. Import your repo on [Vercel](https://vercel.com)
2. Set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Add env var: `VITE_API_URL=https://your-backend.onrender.com`

---

## 📁 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app + middleware
│   │   ├── config.py          # Pydantic settings
│   │   ├── security.py        # Rate limiter + API key auth
│   │   ├── routers/
│   │   │   └── upload.py      # POST /api/upload endpoint
│   │   └── services/
│   │       ├── parser.py      # CSV/XLSX → structured text
│   │       ├── ai_engine.py   # Gemini AI summary generation
│   │       └── mailer.py      # Resend email delivery
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main application
│   │   ├── components/
│   │   │   ├── FileUploader.jsx
│   │   │   ├── StatusFeedback.jsx
│   │   │   └── Header.jsx
│   │   ├── main.jsx
│   │   └── index.css          # Design system
│   ├── Dockerfile
│   ├── vite.config.js
│   └── .env.example
├── .github/workflows/ci.yml   # CI/CD pipeline
├── docker-compose.yml
└── README.md
```

---

## 🔑 Environment Variables

See [`backend/.env.example`](backend/.env.example) and [`frontend/.env.example`](frontend/.env.example).

### Required Keys

| Key | Source | Free Tier |
|-----|--------|-----------|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com) | ✅ Yes |
| `RESEND_API_KEY` | [Resend](https://resend.com) | ✅ 100 emails/day |

---

## 📄 License

Built for Rabbitt AI — Internal Tool
