"""Medical Record model for ORM"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class MedicalRecord(Base):
    """Medical Record model for patient health documentation"""
    __tablename__ = "medical_records"

    id = Column(String, primary_key=True, default=lambda: f"r{str(uuid.uuid4())[:8]}")
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    record_type = Column(String(100), nullable=False)  # consultation, lab-test, prescription, follow-up
    date = Column(DateTime, default=datetime.utcnow, index=True)
    notes = Column(Text, nullable=True)
    diagnosis = Column(String, nullable=True)
    recommendations = Column(Text, nullable=True)
    created_by = Column(String, nullable=True)  # doctor name or system
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="medical_records")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "record_type": self.record_type,
            "date": self.date.isoformat() if self.date else None,
            "notes": self.notes,
            "diagnosis": self.diagnosis,
            "recommendations": self.recommendations,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
