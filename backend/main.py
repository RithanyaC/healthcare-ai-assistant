"""
Healthcare AI Assistant Backend - Main Application
Production-ready modular FastAPI application with database support.
Version 2.0: Modular architecture with SQLAlchemy ORM and clean service layer.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

# Import configuration
from app.config.settings import settings

# Import database
from app.database.base import init_db, get_db_context

# Import middleware
from app.middleware.error_handler import ErrorHandlingMiddleware

# Import utilities
from app.utils.logger import setup_logging
from app.utils.seed_data import seed_sample_data

# Import routes
from app.routes import patients, appointments, medical_records, chat

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.SERVER_NAME,
    description="Production-grade Healthcare AI Assistant with multi-agent orchestration",
    version="2.0.0",
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# Add middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and seed sample data on app startup"""
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")

        # Seed sample data if enabled
        if settings.ENABLE_SAMPLE_DATA:
            logger.info("Seeding sample data...")
            with get_db_context() as db:
                seed_sample_data(db)
            logger.info("Sample data seeding completed")
    except Exception as e:
        logger.error(f"Startup error: {e}")
        sys.exit(1)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown"""
    logger.info("Application shutting down...")

# Include routes
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(medical_records.router)
app.include_router(chat.router)

# Root endpoint
@app.get("/")
def root():
    """Root endpoint - API information"""
    return {
        "name": settings.SERVER_NAME,
        "version": "2.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "docs": "/api/docs" if settings.DEBUG else "Not available in production",
        "health_check": "/api/health"
    }

# Health check
@app.get("/api/health")
def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return {
        "status": "healthy",
        "service": settings.SERVER_NAME,
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred" if not settings.DEBUG else str(exc)
            }
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
