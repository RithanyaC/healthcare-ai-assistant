"""Appointment routes - maintains backward compatibility"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.appointment_service import AppointmentService
from app.services.doctor_service import DoctorService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["appointments"])

class BookingRequest(BaseModel):
    patient_id: str
    doctor_id: str
    slot: str
    reason_for_visit: Optional[str] = None

@router.get("/slots")
def find_slots(specialization: str, db: Session = Depends(get_db)):
    """Find available appointment slots by specialization (backward compatible)"""
    try:
        slots = DoctorService.find_available_slots(db, specialization)
        return {
            "success": True,
            "data": slots,
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/appointments")
def create_appointment(req: BookingRequest, db: Session = Depends(get_db)):
    """Book an appointment (backward compatible)"""
    try:
        appointment = AppointmentService.create_appointment(
            db,
            req.patient_id,
            req.doctor_id,
            req.slot,
            reason_for_visit=req.reason_for_visit
        )
        return {
            "success": True,
            "data": appointment.to_dict(),
            "error": None
        }
    except ValueError as e:
        return {
            "success": False,
            "data": None,
            "error": {"code": "BOOKING_FAILED", "message": str(e)}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/appointments/{patient_id}")
def get_patient_appointments(patient_id: str, db: Session = Depends(get_db)):
    """Get all appointments for a patient"""
    try:
        appointments = AppointmentService.get_patient_appointments(db, patient_id)
        return {
            "success": True,
            "data": [a.to_dict() for a in appointments],
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: str, status: str, db: Session = Depends(get_db)):
    """Update appointment status"""
    try:
        appointment = AppointmentService.update_appointment(db, appointment_id, status=status)
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return {
            "success": True,
            "data": appointment.to_dict(),
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
