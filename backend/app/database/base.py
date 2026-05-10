"""
SQLAlchemy base configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

# Create base class for all models to inherit from
Base = declarative_base()

# Create database engine
# For SQLite in development, use StaticPool to avoid threading issues
if settings.DB_DRIVER == "sqlite":
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # For PostgreSQL
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_size=10,
        max_overflow=20
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    """
    Dependency injection function for FastAPI.
    Yields a database session for request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """
    Context manager for manual database session management.
    Usage: with get_db_context() as db: ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables (create if not exist)"""
    try:
        # Import all models to ensure they are registered with Base
        from app.models.patient import Patient
        from app.models.doctor import Doctor
        from app.models.appointment import Appointment
        from app.models.medical_record import MedicalRecord

        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def drop_db():
    """Drop all database tables (use with caution)"""
    Base.metadata.drop_all(bind=engine)
    logger.warning("All database tables dropped")
