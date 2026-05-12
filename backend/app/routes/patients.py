"""Patient routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.patient_service import PatientService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["patients"])

class PatientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None

@router.post("/patients")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    try:
        new_patient = PatientService.create_patient(db, patient.name, patient.email, **patient.dict())
        return {
            "success": True,
            "data": new_patient.to_dict(),
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    """Get patient details"""
    patient = PatientService.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "success": True,
        "data": patient.to_dict(),
        "error": None
    }

@router.get("/patients/{patient_id}/summary")
def get_patient_summary(patient_id: str, db: Session = Depends(get_db)):
    """Get patient summary with appointments and records"""
    summary = PatientService.get_patient_summary(db, patient_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "success": True,
        "data": summary,
        "error": None
    }

@router.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    """Update patient information"""
    try:
        updated = PatientService.update_patient(db, patient_id, **patient_update.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {
            "success": True,
            "data": updated.to_dict(),
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patients")
def list_patients(skip: int = Query(0, ge=0), limit: int = Query(100, le=100), db: Session = Depends(get_db)):
    """List all patients with pagination"""
    patients = PatientService.get_all_patients(db, skip, limit)
    return {
        "success": True,
        "data": [p.to_dict() for p in patients],
        "error": None
    }
