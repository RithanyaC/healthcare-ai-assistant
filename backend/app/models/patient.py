"""Patient model for ORM"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class Patient(Base):
    """Patient model representing a healthcare patient"""
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=lambda: f"p{str(uuid.uuid4())[:8]}")
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    medical_history = Column(String, nullable=True)  # JSON or text
    allergies = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    appointments = relationship("Appointment", back_populates="patient")
    medical_records = relationship("MedicalRecord", back_populates="patient")

    def to_dict(self):
        """Convert to dictionary (exclude relationships by default)"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "age": self.age,
            "gender": self.gender,
            "medical_history": self.medical_history,
            "allergies": self.allergies,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
