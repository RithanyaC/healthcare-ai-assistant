"""Appointment model for ORM"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database.base import Base

class Appointment(Base):
    """Appointment model representing patient-doctor meetings"""
    __tablename__ = "appointments"

    id = Column(String, primary_key=True, default=lambda: f"a{str(uuid.uuid4())[:8]}")
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False, index=True)
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False, index=True)
    slot = Column(String(100), nullable=False)  # "2024-05-09 10:00"
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    notes = Column(String, nullable=True)
    reason_for_visit = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "slot": self.slot,
            "status": self.status,
            "notes": self.notes,
            "reason_for_visit": self.reason_for_visit,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
