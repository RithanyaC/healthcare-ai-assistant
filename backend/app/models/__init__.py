"""Database models package"""
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord

__all__ = ["Patient", "Doctor", "Appointment", "MedicalRecord"]
