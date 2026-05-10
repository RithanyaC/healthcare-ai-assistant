"""Appointment service for managing appointments"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.appointment import Appointment
from app.services.doctor_service import DoctorService
import logging

logger = logging.getLogger(__name__)

class AppointmentService:
    """Business logic for appointment operations"""

    @staticmethod
    def create_appointment(
        db: Session,
        patient_id: str,
        doctor_id: str,
        slot: str,
        **kwargs
    ) -> Appointment:
        """Create a new appointment"""
        try:
            # Book the doctor's slot
            if not DoctorService.book_slot(db, doctor_id, slot):
                raise ValueError("Slot is not available or doctor not found")

            appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                slot=slot,
                reason_for_visit=kwargs.get("reason_for_visit"),
                notes=kwargs.get("notes")
            )
            db.add(appointment)
            db.commit()
            db.refresh(appointment)
            logger.info(f"Appointment created: {appointment.id}")
            return appointment
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating appointment: {e}")
            raise

    @staticmethod
    def get_appointment(db: Session, appointment_id: str) -> Optional[Appointment]:
        """Get appointment by ID"""
        return db.query(Appointment).filter(Appointment.id == appointment_id).first()

    @staticmethod
    def get_patient_appointments(db: Session, patient_id: str) -> List[Appointment]:
        """Get all appointments for a patient"""
        return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()

    @staticmethod
    def get_upcoming_appointments(db: Session, patient_id: str) -> List[Appointment]:
        """Get upcoming appointments for a patient"""
        return db.query(Appointment).filter(
            Appointment.patient_id == patient_id,
            Appointment.status == "scheduled"
        ).all()

    @staticmethod
    def update_appointment(db: Session, appointment_id: str, **kwargs) -> Optional[Appointment]:
        """Update appointment"""
        try:
            appointment = AppointmentService.get_appointment(db, appointment_id)
            if not appointment:
                return None

            for key, value in kwargs.items():
                if hasattr(appointment, key) and value is not None:
                    setattr(appointment, key, value)

            db.commit()
            db.refresh(appointment)
            logger.info(f"Appointment updated: {appointment_id}")
            return appointment
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating appointment: {e}")
            raise

    @staticmethod
    def cancel_appointment(db: Session, appointment_id: str) -> bool:
        """Cancel an appointment"""
        try:
            appointment = AppointmentService.get_appointment(db, appointment_id)
            if not appointment:
                return False

            appointment.status = "cancelled"
            db.commit()
            logger.info(f"Appointment cancelled: {appointment_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error cancelling appointment: {e}")
            raise
