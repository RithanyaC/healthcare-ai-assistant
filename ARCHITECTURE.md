# Architecture Documentation

## Overview

Healthcare AI Assistant is a production-grade AI-powered healthcare platform built with:
- **Backend**: FastAPI + SQLAlchemy ORM
- **Frontend**: Next.js + React + TypeScript
- **MCP Server**: Agent-based AI orchestration
- **Database**: PostgreSQL (production) / SQLite (development)

## Architecture Layers

### 1. Frontend Architecture (Next.js + React)

```
frontend/
├── app/                      # Next.js app directory
│   ├── layout.tsx           # Root layout with providers
│   ├── page.tsx             # Home page
│   └── chat/
│       └── page.tsx         # Chat interface
├── components/              # React components
│   ├── ChatBox.tsx          # Main chat interface
│   └── ui/
│       └── Components.tsx   # Reusable UI components
├── lib/                     # Utility libraries
│   ├── types/
│   │   └── index.ts         # TypeScript type definitions
│   ├── services/
│   │   └── api.ts           # API service layer
│   ├── hooks/
│   │   └── index.ts         # Custom React hooks
│   └── utils/
│       └── helpers.ts       # Utility functions
└── public/                  # Static assets
```

**Key Pattern**: Service Layer Abstraction
- All API communication goes through `lib/services/api.ts`
- Components use custom hooks (`useChat`, `useToast`, `useAsync`)
- Type-safe throughout with comprehensive TypeScript interfaces

**Benefits**:
- Easy to swap backend implementations (mock, real API, WebSocket)
- Frontend is decoupled from backend URL/protocol
- Reusable state logic via custom hooks
- Zero prop-drilling via hook pattern

### 2. Backend Architecture (FastAPI + SQLAlchemy)

```
backend/
├── main.py                  # FastAPI application entry point
└── app/
    ├── config/
    │   └── settings.py      # Environment-based configuration
    ├── database/
    │   └── base.py          # SQLAlchemy setup and session management
    ├── models/              # SQLAlchemy ORM models
    │   ├── patient.py
    │   ├── doctor.py
    │   ├── appointment.py
    │   └── medical_record.py
    ├── services/            # Business logic layer
    │   ├── patient_service.py
    │   ├── doctor_service.py
    │   ├── appointment_service.py
    │   └── medical_record_service.py
    ├── routes/              # API route handlers
    │   ├── patients.py
    │   ├── appointments.py
    │   ├── medical_records.py
    │   └── chat.py
    ├── middleware/
    │   └── error_handler.py  # Global error handling
    └── utils/
        ├── logger.py        # Logging configuration
        └── seed_data.py     # Sample data generation
```

**Key Pattern**: Modular Service Layer
- Routes → Services → Models pattern
- Services encapsulate business logic
- Models are pure SQLAlchemy ORM definitions
- Database access through SQLAlchemy only

**Benefits**:
- Easy to test (services are independent)
- Clear separation of concerns
- Easy to add new features (new service + route)
- No tight coupling between layers

### 3. MCP Server Architecture (Agent-Based)

```
mcp-server/
├── server.py                 # FastAPI application with orchestration
├── app/
│   ├── config/
│   │   └── settings.py       # MCP configuration
│   ├── tools/                # Tool registry pattern
│   │   ├── registry.py       # Tool abstract base and registry
│   │   └── healthcare_tools.py # Concrete tool implementations
│   └── agents/               # Agent pattern
│       ├── base.py           # Agent framework and intent routing
│       └── healthcare_agents.py # Concrete agent implementations
```

**Key Pattern**: Tool Registry + Agent Router
- Tools are registered and discoverable
- Agents are matched to intents
- New tools/agents can be added without modifying router
- Backward-compatible legacy endpoints

**Benefits**:
- Scalable agent system
- Tools are reusable across agents
- Intent detection is extensible
- Full COIN protocol logging for debugging

## Data Flow

### Chat Message Flow

```
1. User sends message in ChatBox component
   ↓
2. useChat hook calls chatService.sendMessage()
   ↓
3. API service layer sends POST /api/chat to backend
   ↓
4. Backend routes to chat route, forwards to MCP server
   ↓
5. MCP server:
   - Detects intent from message (IntentDetector)
   - Routes to appropriate agent (AgentRouter)
   - Agent executes corresponding tool
   - Returns formatted response with logs
   ↓
6. Backend returns response to frontend
   ↓
7. useChat updates message state
   ↓
8. ChatBox displays message and logs
```

### Database Operations Flow

```
Frontend Component
   ↓
API Service Layer (lib/services/api.ts)
   ↓
FastAPI Route Handler (/api/...)
   ↓
Service Layer (app/services/*.py)
   ↓
SQLAlchemy Models (app/models/*.py)
   ↓
Database Engine (SQLite/PostgreSQL)
```

## Database Schema

### Patient
- `id`: Primary key
- `name`, `email`, `phone`: Contact information
- `age`, `gender`: Demographics
- `medical_history`, `allergies`: Medical info (JSON)
- `is_active`: Soft delete flag
- `created_at`, `updated_at`: Timestamps

### Doctor
- `id`: Primary key
- `name`, `email`: Contact information
- `specialization`: Medical specialty
- `license_number`: Professional credential
- `experience_years`: Years of experience
- `available_slots`: JSON array of availability
- `rating`: Patient rating
- `created_at`, `updated_at`: Timestamps

### Appointment
- `id`: Primary key
- `patient_id`: Foreign key to Patient
- `doctor_id`: Foreign key to Doctor
- `slot`: Appointment time
- `status`: pending/confirmed/completed/cancelled
- `notes`, `reason_for_visit`: Appointment details
- `created_at`, `updated_at`: Timestamps

### MedicalRecord
- `id`: Primary key
- `patient_id`: Foreign key to Patient
- `record_type`: consultation/lab/imaging/prescription
- `date`: Record date
- `notes`: Doctor notes
- `diagnosis`: Medical diagnosis
- `recommendations`: Treatment recommendations
- `created_by`: Doctor ID
- `created_at`, `updated_at`: Timestamps

## API Contract

### Request/Response Format

All API responses follow consistent format:
```json
{
  "success": boolean,
  "data": any,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/chat` | Send chat message to MCP orchestrator |
| GET | `/api/patients/{id}/summary` | Get patient medical summary |
| GET | `/api/slots` | Find available appointment slots |
| POST | `/api/appointments` | Book appointment |
| POST | `/api/followups` | Create follow-up reminder |
| GET | `/api/health` | Health check endpoint |

## Backward Compatibility

The refactored system maintains full backward compatibility:
- Original API endpoints remain unchanged
- Response format is identical
- Legacy `patient_id: "p1"` patient identifier still works
- MCP server has legacy tool endpoints alongside new orchestration

## Environment Configuration

### Backend
- `ENVIRONMENT`: development/production
- `DB_DRIVER`: sqlite/postgresql
- `SECRET_KEY`: JWT signing key
- `MCP_SERVER_URL`: MCP server location
- See `backend/.env.example` for full list

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_MCP_URL`: MCP server URL
- See `frontend/.env.local.example` for full list

### MCP Server
- `ENVIRONMENT`: development/production
- `BACKEND_URL`: Backend API URL
- See `mcp-server/.env.example` for full list

## Deployment

### Docker Deployment
```bash
docker-compose up
```

Services:
- `postgres`: PostgreSQL database (port 5432)
- `backend`: FastAPI backend (port 8000)
- `mcp`: MCP server (port 8001)
- `frontend`: Next.js frontend (port 3000)

### Development Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev

# MCP Server
cd mcp-server
pip install -r requirements.txt
python -m uvicorn server:app --reload --port 8001
```

## Security

- JWT authentication support (infrastructure ready)
- CORS configuration per environment
- SQL injection protection via SQLAlchemy ORM
- XSS protection via React/Next.js
- HTTPS in production (via reverse proxy)

## Monitoring & Logging

- Structured logging via Python logging
- Health check endpoints on all services
- Docker health checks with automatic restarts
- Agent action logging via COIN protocol
- Error handling with consistent response format

## Future Enhancements

1. **Authentication**: JWT tokens + RBAC
2. **Real-time**: WebSocket integration
3. **LLM Integration**: OpenAI API for advanced agent reasoning
4. **Search**: Full-text and semantic search for medical records
5. **Notifications**: Email/SMS appointment reminders
6. **Reporting**: Patient and doctor dashboards
7. **Analytics**: Usage metrics and insights
