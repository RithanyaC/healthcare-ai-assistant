# Deployment Guide

## Production Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        VERCEL FRONTEND                          │
│         https://healthcare-ai-assistant-beta.vercel.app         │
│              (Next.js - NEXT_PUBLIC_* env vars)                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┴──────────────────┐
        │ NEXT_PUBLIC_MCP_URL                 │ NEXT_PUBLIC_API_URL
        │ (for /chat, /orchestrate)          │ (for patient data)
        │                                     │
        ▼                                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RENDER MCP SERVER                            │
│     https://healthcare-ai-assistant-r0mw.onrender.com           │
│         FastAPI - Tool orchestration & Agents                   │
│         (BACKEND_URL env var points to Backend API)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    requests.get/post
                    (BACKEND_URL env var)
                           │
        ┌──────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RENDER BACKEND API                           │
│    https://healthcare-ai-assistant-1.onrender.com               │
│    FastAPI - Core services, appointments, patient data          │
│    (MCP_SERVER_URL env var points to MCP Server)                │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- Docker and Docker Compose (for container deployment)
- Python 3.11+ (for local development)
- Node.js 22+ (for frontend development)
- PostgreSQL 16+ (for production database)
- Git for version control

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd healthcare-ai-assistant
```

### 2. Configure Environment Variables

#### Backend
```bash
cd backend
cp .env.example .env
```

Edit `backend/.env`:
```
ENVIRONMENT=development
DEBUG=true
MCP_SERVER_URL=http://localhost:8001
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
DB_DRIVER=sqlite
```

#### MCP Server
```bash
cd ../mcp-server
cp .env.example .env
```

Edit `mcp-server/.env`:
```
ENVIRONMENT=development
DEBUG=true
BACKEND_URL=http://localhost:8000
```

#### Frontend
```bash
cd ../frontend
cp .env.local.example .env.local
```

Edit `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MCP_URL=http://localhost:8001
```

### 3. Install Dependencies & Run Services (3 terminal windows)

#### Terminal 1: Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Runs on: http://localhost:8000

#### Terminal 2: MCP Server
```bash
cd mcp-server
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn server:app --reload --port 8001
```
Runs on: http://localhost:8001

#### Terminal 3: Frontend
```bash
cd frontend
npm install
npm run dev
```
Runs on: http://localhost:3000

### 4. Verify Setup
```bash
# Check backend health
curl http://localhost:8000/api/health

# Check MCP health
curl http://localhost:8001/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache", "patient_id": "p1"}'
```

## Docker Compose Development

### Quick Start
```bash
cp backend/.env.example backend/.env
cp mcp-server/.env.example mcp-server/.env
cp frontend/.env.local.example frontend/.env.local

docker-compose up
```

Services available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- MCP Server: http://localhost:8001
- Database: localhost:5432

## Production Deployment on Render

### Prerequisites
- Render.com account
- GitHub repository with code

### 1. Deploy Backend API to Render

1. Go to https://dashboard.render.com
2. Create new **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: healthcare-ai-assistant-1
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000`
   - **Root Directory**: `backend/`
   - **Environment Variables**:
     ```
     ENVIRONMENT=production
     DEBUG=false
     MCP_SERVER_URL=https://healthcare-ai-assistant-r0mw.onrender.com
     ALLOWED_ORIGINS=https://healthcare-ai-assistant-beta.vercel.app
     DB_DRIVER=sqlite
     SECRET_KEY=<generate-secure-key>
     ```

5. Deploy

### 2. Deploy MCP Server to Render

1. Create new **Web Service**
2. Configure:
   - **Name**: healthcare-ai-assistant
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:8001`
   - **Root Directory**: `mcp-server/`
   - **Environment Variables**:
     ```
     ENVIRONMENT=production
     DEBUG=false
     BACKEND_URL=https://healthcare-ai-assistant-1.onrender.com
     LOG_LEVEL=INFO
     ```

3. Deploy

### 3. Deploy Frontend to Vercel

1. Go to https://vercel.com
2. Import project from GitHub
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend/`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=https://healthcare-ai-assistant-1.onrender.com
     NEXT_PUBLIC_MCP_URL=https://healthcare-ai-assistant-r0mw.onrender.com
     ```

4. Deploy

## Service Communication Verification

### Test Production Endpoints

```bash
# Check backend health
curl https://healthcare-ai-assistant-1.onrender.com/api/health

# Check MCP health
curl https://healthcare-ai-assistant-r0mw.onrender.com/health

# Test chat via MCP
curl -X POST https://healthcare-ai-assistant-r0mw.onrender.com/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache", "patient_id": "p1"}'
```

## Environment Variables Reference

### Backend (.env)
| Variable | Development | Production | Description |
|----------|-------------|-----------|-------------|
| ENVIRONMENT | development | production | Environment type |
| DEBUG | true | false | Debug mode |
| MCP_SERVER_URL | http://localhost:8001 | https://healthcare-ai-assistant-r0mw.onrender.com | MCP Server URL |
| ALLOWED_ORIGINS | http://localhost:3000,http://localhost:3001 | https://healthcare-ai-assistant-beta.vercel.app | CORS allowed origins |
| DB_DRIVER | sqlite | postgresql | Database driver |
| DATABASE_URL | sqlite:///./healthcare.db | postgresql://... | Database connection |

### MCP Server (.env)
| Variable | Development | Production | Description |
|----------|-------------|-----------|-------------|
| ENVIRONMENT | development | production | Environment type |
| DEBUG | true | false | Debug mode |
| BACKEND_URL | http://localhost:8000 | https://healthcare-ai-assistant-1.onrender.com | Backend API URL |
| LOG_LEVEL | INFO | INFO | Logging level |

### Frontend (.env.local)
| Variable | Development | Production | Description |
|----------|-------------|-----------|-------------|
| NEXT_PUBLIC_API_URL | http://localhost:8000 | https://healthcare-ai-assistant-1.onrender.com | Backend API URL |
| NEXT_PUBLIC_MCP_URL | http://localhost:8001 | https://healthcare-ai-assistant-r0mw.onrender.com | MCP Server URL |

## Monitoring & Troubleshooting

### Common Issues

#### CORS Errors
```
Error: Access to XMLHttpRequest has been blocked by CORS policy
Solution: Check ALLOWED_ORIGINS includes your frontend URL
          Restart backend after changing configuration
```

#### MCP Connection Errors
```
Error: AI orchestration service is unavailable
Solution: Verify BACKEND_URL in MCP .env is correct
         Check backend MCP_SERVER_URL matches MCP URL
```

#### Frontend API 404 Errors
```
Error: 404 Not Found
Solution: Verify NEXT_PUBLIC_API_URL in frontend/.env.local
         Check backend service is running and accessible
```

### Health Check Endpoints

- Backend: `https://healthcare-ai-assistant-1.onrender.com/api/health`
- MCP: `https://healthcare-ai-assistant-r0mw.onrender.com/health`

### View Logs

**Render Services**:
- Go to service dashboard → Logs
- Real-time logs visible in the UI

**Local Docker**:
```bash
docker-compose logs -f backend
docker-compose logs -f mcp
docker-compose logs -f frontend
```

## Scaling Considerations

### Load Balancing
- Render automatically scales services with increased traffic
- Frontend is served globally via Vercel's CDN

### Database
- Start with SQLite (development/small scale)
- Upgrade to PostgreSQL for production multi-instance setups
- Enable connection pooling for multiple backend instances

### Performance
- MCP caches agent responses
- Frontend uses Next.js static generation where possible
- Consider adding Redis for session management

## Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **Secrets**: Use Render/Vercel secrets management
3. **CORS**: Specify exact origins, don't use "*" in production
4. **SSL/TLS**: All production endpoints should use HTTPS
5. **API Keys**: Store LLM keys securely in environment variables
3. **API caching**: Add caching headers and ETag support

## Backup & Recovery

### Database Backups

```bash
# PostgreSQL backup
pg_dump healthcare_db > backup.sql

# Restore
psql healthcare_db < backup.sql

# Docker backup
docker exec healthcare-db pg_dump healthcare_db > backup.sql
```

### Application Backups

```bash
# Backup environment files
tar -czf config-backup.tar.gz backend/.env mcp-server/.env frontend/.env.local

# Backup database volume
docker run --rm -v postgres_data:/data -v $(pwd):/backup \
  busybox tar czf /backup/postgres-data.tar.gz /data
```

## Updates & Maintenance

### Rolling Updates (Docker)

```bash
# Update image
docker-compose pull
docker-compose up -d

# Services update without downtime (with health checks)
```

### Zero-Downtime Deployment (Kubernetes)

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

## Security Checklist

- [ ] Change SECRET_KEY to secure random value
- [ ] Set ENVIRONMENT=production
- [ ] Configure ALLOWED_ORIGINS for specific domains
- [ ] Use HTTPS with valid SSL certificate
- [ ] Configure database password to strong value
- [ ] Set up authentication/RBAC (optional)
- [ ] Configure firewall rules
- [ ] Set up regular database backups
- [ ] Configure log aggregation
- [ ] Enable monitoring and alerting

## Support

For issues and questions:
1. Check logs: `docker-compose logs -f <service>`
2. Review ARCHITECTURE.md for design details
3. Check error responses: All errors return consistent JSON format
4. Verify environment configuration: Compare with .env.example files
