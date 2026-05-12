"""Doctor service for managing doctor-related operations"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.models.doctor import Doctor
import logging

logger = logging.getLogger(__name__)

class DoctorService:
    """Business logic for doctor operations"""

    @staticmethod
    def create_doctor(db: Session, name: str, email: str, specialization: str, license_number: str, **kwargs) -> Doctor:
        """Create a new doctor"""
        try:
            doctor = Doctor(
                name=name,
                email=email,
                specialization=specialization,
                license_number=license_number,
                phone=kwargs.get("phone"),
                experience_years=kwargs.get("experience_years"),
                bio=kwargs.get("bio"),
                available_slots=kwargs.get("available_slots", [])
            )
            db.add(doctor)
            db.commit()
            db.refresh(doctor)
            logger.info(f"Doctor created: {doctor.id}")
            return doctor
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating doctor: {e}")
            raise

    @staticmethod
    def get_doctor(db: Session, doctor_id: str) -> Optional[Doctor]:
        """Get doctor by ID"""
        return db.query(Doctor).filter(Doctor.id == doctor_id).first()

    @staticmethod
    def get_all_doctors(db: Session, skip: int = 0, limit: int = 100) -> List[Doctor]:
        """Get all doctors"""
        return db.query(Doctor).filter(Doctor.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def get_doctors_by_specialization(db: Session, specialization: str) -> List[Doctor]:
        """Get doctors by specialization"""
        return db.query(Doctor).filter(
            Doctor.specialization.ilike(f"%{specialization}%"),
            Doctor.is_active == True
        ).all()

    @staticmethod
    def update_doctor(db: Session, doctor_id: str, **kwargs) -> Optional[Doctor]:
        """Update doctor information"""
        try:
            doctor = DoctorService.get_doctor(db, doctor_id)
            if not doctor:
                return None

            for key, value in kwargs.items():
                if hasattr(doctor, key) and value is not None:
                    setattr(doctor, key, value)

            db.commit()
            db.refresh(doctor)
            logger.info(f"Doctor updated: {doctor_id}")
            return doctor
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating doctor: {e}")
            raise

    @staticmethod
    def find_available_slots(db: Session, specialization: str) -> List[Dict[str, Any]]:
        """Find available appointment slots by specialization"""
        doctors = DoctorService.get_doctors_by_specialization(db, specialization)
        available_slots = []

        for doctor in doctors:
            if doctor.available_slots:
                for slot in doctor.available_slots:
                    available_slots.append({
                        "doctor_id": doctor.id,
                        "doctor_name": doctor.name,
                        "specialization": doctor.specialization,
                        "slot": slot
                    })

        return available_slots

    @staticmethod
    def book_slot(db: Session, doctor_id: str, slot: str) -> bool:
        """Book a specific slot for a doctor"""
        try:
            doctor = DoctorService.get_doctor(db, doctor_id)
            if not doctor or slot not in doctor.available_slots:
                return False

            doctor.available_slots.remove(slot)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error booking slot: {e}")
            raise
