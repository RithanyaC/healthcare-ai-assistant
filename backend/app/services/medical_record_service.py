"""Medical record service for managing patient health records"""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.medical_record import MedicalRecord
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MedicalRecordService:
    """Business logic for medical record operations"""

    @staticmethod
    def create_record(
        db: Session,
        patient_id: str,
        record_type: str,
        notes: str,
        **kwargs
    ) -> MedicalRecord:
        """Create a new medical record"""
        try:
            record = MedicalRecord(
                patient_id=patient_id,
                record_type=record_type,
                notes=notes,
                diagnosis=kwargs.get("diagnosis"),
                recommendations=kwargs.get("recommendations"),
                created_by=kwargs.get("created_by", "system")
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            logger.info(f"Medical record created: {record.id}")
            return record
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating medical record: {e}")
            raise

    @staticmethod
    def get_record(db: Session, record_id: str) -> Optional[MedicalRecord]:
        """Get record by ID"""
        return db.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()

    @staticmethod
    def get_patient_records(
        db: Session,
        patient_id: str,
        record_type: Optional[str] = None,
        limit: int = 10
    ) -> List[MedicalRecord]:
        """Get medical records for a patient"""
        query = db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id)

        if record_type:
            query = query.filter(MedicalRecord.record_type == record_type)

        return query.order_by(MedicalRecord.date.desc()).limit(limit).all()

    @staticmethod
    def create_followup(
        db: Session,
        patient_id: str,
        notes: str,
        **kwargs
    ) -> MedicalRecord:
        """Create a follow-up record"""
        return MedicalRecordService.create_record(
            db,
            patient_id,
            "follow-up",
            notes,
            created_by=kwargs.get("created_by", "system"),
            recommendations=kwargs.get("recommendations")
        )
