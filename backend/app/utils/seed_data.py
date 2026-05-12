"""Data seeding utilities for development"""
from sqlalchemy.orm import Session
from app.services.patient_service import PatientService
from app.services.doctor_service import DoctorService
import logging

logger = logging.getLogger(__name__)

def seed_sample_data(db: Session):
    """Seed database with sample data for testing"""
    try:
        # Create sample doctors
        doctors_data = [
            {
                "name": "Dr. Sarah Johnson",
                "email": "sarah.johnson@healthcare.com",
                "specialization": "Cardiology",
                "license_number": "LIC001",
                "experience_years": 12,
                "bio": "Specialist in heart and cardiovascular diseases",
                "available_slots": ["2024-05-10 10:00", "2024-05-10 14:00", "2024-05-11 09:00"]
            },
            {
                "name": "Dr. Michael Chen",
                "email": "michael.chen@healthcare.com",
                "specialization": "Neurology",
                "license_number": "LIC002",
                "experience_years": 8,
                "bio": "Expert in neurological disorders",
                "available_slots": ["2024-05-10 11:00", "2024-05-10 15:00"]
            },
            {
                "name": "Dr. Emily Rodriguez",
                "email": "emily.rodriguez@healthcare.com",
                "specialization": "General Physician",
                "license_number": "LIC003",
                "experience_years": 6,
                "bio": "Primary care physician",
                "available_slots": ["2024-05-10 09:00", "2024-05-10 13:00", "2024-05-11 10:00"]
            }
        ]

        for doc_data in doctors_data:
            try:
                existing = DoctorService.get_doctors_by_specialization(db, doc_data["specialization"])
                if not any(d.email == doc_data["email"] for d in existing):
                    DoctorService.create_doctor(db, **doc_data)
                    logger.info(f"Doctor created: {doc_data['name']}")
            except Exception as e:
                logger.warning(f"Doctor creation skipped: {doc_data['name']} - {e}")

        # Create sample patients
        patients_data = [
            {
                "id": "p1",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+1-555-0101",
                "age": 35,
                "gender": "Male",
                "medical_history": "No major conditions",
                "allergies": "Penicillin"
            },
            {
                "id": "p2",
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+1-555-0102",
                "age": 28,
                "gender": "Female",
                "medical_history": "Asthma",
                "allergies": "None"
            }
        ]

        for pat_data in patients_data:
            try:
                if not PatientService.get_patient(db, pat_data.get("id", "")):
                    PatientService.create_patient(db, **pat_data)
                    logger.info(f"Patient created: {pat_data['name']}")
            except Exception as e:
                logger.warning(f"Patient creation skipped: {pat_data['name']} - {e}")

        logger.info("Sample data seeding completed")
    except Exception as e:
        logger.error(f"Error seeding sample data: {e}")
        raise
