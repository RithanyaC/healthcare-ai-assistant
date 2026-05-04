# Healthcare AI Assistant

A production-grade Healthcare AI Assistant system with multi-agent orchestration.

## Architecture

1. **Frontend (Next.js)**: Modern chat UI with rich aesthetics.
2. **Backend (FastAPI)**: Core services, data management, and orchestrator.
3. **MCP Server (FastAPI)**: Exposes AI tools used by the orchestrator.
4. **Data**: JSON based data storage.

## How to Run

You will need 3 terminal windows.

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --port 8000 --reload
```

### 2. MCP Server
```bash
cd mcp-server
pip install -r requirements.txt
uvicorn server:app --port 8001 --reload
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

## Demo Flow

1. Open http://localhost:3000
2. Click "Start Consultation"
3. Try saying:
   - "I have severe chest pain" (Triggers Triage Agent)
   - "Book a doctor tomorrow" (Triggers Scheduling Agent)
   - "Show my medical summary" (Triggers Summary Agent)
   - "Remind me to follow up" (Triggers Follow-up Agent)
