# Deployment Guide

## Prerequisites

- Docker and Docker Compose (for container deployment)
- Python 3.11+ (for local development)
- Node.js 22+ (for frontend development)
- PostgreSQL 16+ (for production database)

## Quick Start with Docker Compose

### 1. Clone Repository
```bash
git clone <repository-url>
cd healthcare-ai-assistant
```

### 2. Configure Environment Variables

Create `.env` files from examples:

```bash
# Backend
cp backend/.env.example backend/.env

# MCP Server
cp mcp-server/.env.example mcp-server/.env

# Frontend
cp frontend/.env.local.example frontend/.env.local
```

Edit files as needed for your environment.

### 3. Start Services
```bash
docker-compose up
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- MCP Server: http://localhost:8001
- Database: localhost:5432

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

## Local Development Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run with auto-reload
python -m uvicorn main:app --reload
```

Backend will run on http://localhost:8000

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Edit .env.local with your settings

# Run development server
npm run dev
```

Frontend will run on http://localhost:3000

### MCP Server

```bash
cd mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run with auto-reload
python -m uvicorn server:app --reload --port 8001
```

MCP Server will run on http://localhost:8001

## Production Deployment

### Using Docker Compose (Recommended)

1. **Set production environment variables**:
```bash
# In docker-compose.yml, update:
# - ENVIRONMENT=production
# - Update SECRET_KEY with secure value
# - Configure database credentials
```

2. **Use production images**:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

3. **Set up reverse proxy** (nginx recommended):
```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

upstream mcp {
    server mcp:8001;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # MCP Server
    location /mcp/ {
        proxy_pass http://mcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Kubernetes Deployment

1. **Build images**:
```bash
docker build -f Dockerfile.backend -t healthcare-backend:latest .
docker build -f Dockerfile.frontend -t healthcare-frontend:latest .
docker build -f Dockerfile.mcp -t healthcare-mcp:latest .

# Push to registry
docker push <registry>/healthcare-backend:latest
docker push <registry>/healthcare-frontend:latest
docker push <registry>/healthcare-mcp:latest
```

2. **Create Kubernetes manifests** (example):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: backend
        image: healthcare-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DB_DRIVER
          value: "postgresql"
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
```

3. **Deploy**:
```bash
kubectl apply -f k8s/
```

## Database Setup

### SQLite (Development)

SQLite database is created automatically on first run.

### PostgreSQL (Production)

1. **Create database**:
```sql
CREATE DATABASE healthcare_db;
CREATE USER healthcare WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare;
```

2. **Run migrations**:
```bash
cd backend
alembic upgrade head
```

3. **Seed initial data** (optional):
```bash
ENABLE_SAMPLE_DATA=true python -m uvicorn main:app
```

## Monitoring

### Health Checks

All services expose health check endpoints:

```bash
# Backend
curl http://localhost:8000/api/health

# MCP
curl http://localhost:8001/health
```

### Logs

View service logs:
```bash
# Using Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mcp

# Using Docker
docker logs -f healthcare-backend
docker logs -f healthcare-frontend
docker logs -f healthcare-mcp
```

### Performance Monitoring

1. **Backend metrics**: Add Prometheus integration
2. **Frontend metrics**: Add Google Analytics or Sentry
3. **Database metrics**: Use PostgreSQL pg_stat_statements

## Troubleshooting

### Backend Connection Errors

**Problem**: Backend can't connect to database
```
Solution: Check DATABASE_URL in .env matches actual database location
```

**Problem**: MCP can't connect to backend
```
Solution: Verify BACKEND_URL in MCP .env matches backend location
         Check ALLOWED_ORIGINS includes MCP server address
```

### Frontend API Errors

**Problem**: Frontend shows 404 errors
```
Solution: Check NEXT_PUBLIC_API_URL in .env.local
         Verify backend is running and accessible
```

**Problem**: CORS errors in browser console
```
Solution: Check backend ALLOWED_ORIGINS includes frontend URL
         Restart backend after changing configuration
```

### Database Issues

**Problem**: "permission denied" errors
```
Solution: Verify database user has correct permissions:
         GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare;
```

**Problem**: Migration conflicts
```
Solution: Reset database (development only):
         alembic downgrade base
         alembic upgrade head
```

## Scaling

### Horizontal Scaling

1. **Backend**: Run multiple instances behind load balancer
2. **Frontend**: Static site can be served from CDN
3. **Database**: Use read replicas for read-heavy workloads

### Vertical Scaling

1. **Increase service resources**: CPU/memory in docker-compose or Kubernetes
2. **Increase database connections**: Adjust connection pool size in settings.py

### Caching

1. **Add Redis**: For session caching and rate limiting
2. **Frontend caching**: Use Next.js built-in static generation
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
