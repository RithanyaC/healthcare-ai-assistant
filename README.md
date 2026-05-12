# Healthcare AI Assistant

A production-grade Healthcare AI Assistant system with multi-agent orchestration, deployed across Vercel (frontend), Render (backend & MCP server).

## Architecture

1. **Frontend (Next.js)**: Modern chat UI with rich aesthetics, deployed on Vercel
2. **Backend (FastAPI)**: Core services, data management, and orchestrator on Render
3. **MCP Server (FastAPI)**: Exposes AI tools used by the orchestrator on Render
4. **Data**: JSON based data storage

## Deployment

### Production Deployment
- **Frontend**: https://healthcare-ai-assistant-beta.vercel.app/
- **Backend API**: https://healthcare-ai-assistant-1.onrender.com
- **MCP Server**: https://healthcare-ai-assistant-r0mw.onrender.com

## How to Run

### Development (3 terminal windows)

#### 1. Backend
```bash
cd backend
cp .env.example .env
# Edit .env with development settings
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
```

#### 2. MCP Server
```bash
cd mcp-server
cp .env.example .env
# Edit .env with development settings
pip install -r requirements.txt
uvicorn server:app --port 8001 --reload
```

#### 3. Frontend
```bash
cd frontend
cp .env.local.example .env.local
# Edit .env.local with development settings
npm install
npm run dev
```

Access the application at http://localhost:3000

## Environment Variables

### Backend (.env)
- `ENVIRONMENT`: development, production, or testing
- `MCP_SERVER_URL`: URL of the MCP server (dev: http://localhost:8001, prod: https://healthcare-ai-assistant-r0mw.onrender.com)
- `ALLOWED_ORIGINS`: CORS allowed origins (include your frontend URL)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT secret key

### MCP Server (.env)
- `BACKEND_URL`: URL of the backend API (dev: http://localhost:8000, prod: https://healthcare-ai-assistant-1.onrender.com)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API URL (dev: http://localhost:8000, prod: https://healthcare-ai-assistant-1.onrender.com)
- `NEXT_PUBLIC_MCP_URL`: MCP server URL (dev: http://localhost:8001, prod: https://healthcare-ai-assistant-r0mw.onrender.com)

## Service Communication Flow

```
Frontend
  ↓ (chat messages)
  ↓ fetch to NEXT_PUBLIC_MCP_URL/chat or /orchestrate
  ↓
MCP Server (Agent Orchestration)
  ↓ (tool execution requests)
  ↓ requests to BACKEND_URL/api/*
  ↓
Backend API
  ↓ (responses)
  ↓ returns to MCP Server
  ↓
MCP Server
  ↓ (agent responses)
  ↓ returns to Frontend
  ↓
Frontend (displays results)
```

## Demo Flow

1. Open http://localhost:3000 (or production URL)
2. Click "Start Consultation"
3. Try saying:
   - "I have severe chest pain" (Triggers Triage Agent)
   - "Book a doctor tomorrow" (Triggers Scheduling Agent)
   - "Show my medical summary" (Triggers Summary Agent)
   - "Remind me to follow up" (Triggers Follow-up Agent)
