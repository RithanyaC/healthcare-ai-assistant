"""Patient service for managing patient-related operations"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.patient import Patient
from app.database.base import get_db_context
import logging

logger = logging.getLogger(__name__)

class PatientService:
    """Business logic for patient operations"""

    @staticmethod
    def create_patient(db: Session, name: str, email: str, **kwargs) -> Patient:
        """Create a new patient"""
        try:
            patient = Patient(
                name=name,
                email=email,
                phone=kwargs.get("phone"),
                age=kwargs.get("age"),
                gender=kwargs.get("gender"),
                medical_history=kwargs.get("medical_history"),
                allergies=kwargs.get("allergies")
            )
            db.add(patient)
            db.commit()
            db.refresh(patient)
            logger.info(f"Patient created: {patient.id}")
            return patient
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating patient: {e}")
            raise

    @staticmethod
    def get_patient(db: Session, patient_id: str) -> Optional[Patient]:
        """Get patient by ID"""
        return db.query(Patient).filter(Patient.id == patient_id).first()

    @staticmethod
    def get_patient_by_email(db: Session, email: str) -> Optional[Patient]:
        """Get patient by email"""
        return db.query(Patient).filter(Patient.email == email).first()

    @staticmethod
    def get_all_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Get all patients with pagination"""
        return db.query(Patient).offset(skip).limit(limit).all()

    @staticmethod
    def update_patient(db: Session, patient_id: str, **kwargs) -> Optional[Patient]:
        """Update patient information"""
        try:
            patient = PatientService.get_patient(db, patient_id)
            if not patient:
                return None

            for key, value in kwargs.items():
                if hasattr(patient, key) and value is not None:
                    setattr(patient, key, value)

            db.commit()
            db.refresh(patient)
            logger.info(f"Patient updated: {patient_id}")
            return patient
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating patient: {e}")
            raise

    @staticmethod
    def delete_patient(db: Session, patient_id: str) -> bool:
        """Delete a patient (soft delete by setting inactive)"""
        try:
            patient = PatientService.get_patient(db, patient_id)
            if not patient:
                return False

            patient.is_active = False
            db.commit()
            logger.info(f"Patient deactivated: {patient_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting patient: {e}")
            raise

    @staticmethod
    def get_patient_summary(db: Session, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive patient summary (appointments + records)"""
        from app.models.appointment import Appointment
        from app.models.medical_record import MedicalRecord

        patient = PatientService.get_patient(db, patient_id)
        if not patient:
            return None

        records = db.query(MedicalRecord).filter(
            MedicalRecord.patient_id == patient_id
        ).order_by(MedicalRecord.date.desc()).limit(5).all()

        appointments = db.query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.status != "completed"
        ).all()

        return {
            "patient": patient.to_dict(),
            "recent_records": [r.to_dict() for r in records],
            "upcoming_appointments": [a.to_dict() for a in appointments]
        }
