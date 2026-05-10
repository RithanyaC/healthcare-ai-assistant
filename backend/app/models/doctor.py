"""Doctor model for ORM"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class Doctor(Base):
    """Doctor model representing a healthcare professional"""
    __tablename__ = "doctors"

    id = Column(String, primary_key=True, default=lambda: f"d{str(uuid.uuid4())[:8]}")
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    specialization = Column(String(100), nullable=False, index=True)
    license_number = Column(String(100), unique=True, nullable=False)
    experience_years = Column(Integer, nullable=True)
    bio = Column(String, nullable=True)
    available_slots = Column(JSON, default=list)  # ["2024-05-09 10:00", "2024-05-09 11:00"]
    is_active = Column(Boolean, default=True)
    rating = Column(Integer, default=0)  # 0-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="doctor")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "specialization": self.specialization,
            "license_number": self.license_number,
            "experience_years": self.experience_years,
            "bio": self.bio,
            "available_slots": self.available_slots,
            "is_active": self.is_active,
            "rating": self.rating,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
