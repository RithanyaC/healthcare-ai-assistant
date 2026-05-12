"""Medical records routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.base import get_db
from app.services.medical_record_service import MedicalRecordService
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api", tags=["medical-records"])

class FollowupRequest(BaseModel):
    patient_id: str
    notes: str
    recommendations: Optional[str] = None

@router.post("/followups")
def create_followup(req: FollowupRequest, db: Session = Depends(get_db)):
    """Create a follow-up record (backward compatible)"""
    try:
        record = MedicalRecordService.create_followup(
            db,
            req.patient_id,
            req.notes,
            recommendations=req.recommendations
        )
        return {
            "success": True,
            "data": record.to_dict(),
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patients/{patient_id}/records")
def get_patient_records(
    patient_id: str,
    record_type: Optional[str] = Query(None),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db)
):
    """Get medical records for a patient"""
    try:
        records = MedicalRecordService.get_patient_records(db, patient_id, record_type, limit)
        return {
            "success": True,
            "data": [r.to_dict() for r in records],
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/patients/{patient_id}/records")
def create_medical_record(
    patient_id: str,
    record_type: str,
    notes: str,
    diagnosis: Optional[str] = None,
    recommendations: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a medical record"""
    try:
        record = MedicalRecordService.create_record(
            db,
            patient_id,
            record_type,
            notes,
            diagnosis=diagnosis,
            recommendations=recommendations
        )
        return {
            "success": True,
            "data": record.to_dict(),
            "error": None
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
