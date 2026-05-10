"""Healthcare-specific tools"""
from app.tools.registry import Tool
from typing import Dict, Any
import requests
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class SymptomCheckerTool(Tool):
    """Tool for checking and assessing patient symptoms"""

    def __init__(self):
        super().__init__(
            name="symptom_check",
            description="Analyze patient symptoms and provide triage assessment",
            required_params=["symptoms"]
        )

    async def execute(self, symptoms: str, **kwargs) -> Dict[str, Any]:
        """
        Execute symptom analysis with improved logic
        Categorizes symptoms and provides risk-based recommendations
        """
        symptoms_lower = symptoms.lower()

        # Emergency symptoms - HIGH RISK
        high_risk_keywords = [
            "chest pain", "shortness of breath", "breathing difficulty", "heart pain",
            "stroke", "paralysis", "seizure", "unconscious", "severe bleeding",
            "difficulty speaking", "loss of vision", "sudden numbness"
        ]

        # Moderate symptoms - MEDIUM RISK
        medium_risk_keywords = [
            "high fever", "persistent cough", "infection", "vomiting", "diarrhea",
            "stomach pain", "abdominal pain", "indigestion", "severe headache",
            "back pain", "joint pain"
        ]

        # Check risk level
        if any(keyword in symptoms_lower for keyword in high_risk_keywords):
            risk_level = "High"
            specialist = "Emergency Medicine / Cardiology / Neurology"
            assessment = "⚠️ URGENT: Symptoms may indicate a serious condition. Seek immediate medical attention."
        elif any(keyword in symptoms_lower for keyword in medium_risk_keywords):
            risk_level = "Medium"
            specialist = "General Physician / Internal Medicine"
            assessment = "⚠️ Symptoms suggest a possible condition. Consult a doctor within 24 hours."
        else:
            risk_level = "Low"
            specialist = "General Physician"
            assessment = "✓ Likely minor condition. Rest, hydrate, and monitor. Consult if it persists."

        return {
            "assessment": assessment,
            "risk_level": risk_level,
            "recommended_specialist": specialist,
            "symptoms_reported": symptoms
        }

class ScheduleAppointmentTool(Tool):
    """Tool for scheduling appointments"""

    def __init__(self):
        super().__init__(
            name="schedule_appointment",
            description="Find available slots and schedule an appointment",
            required_params=["patient_id", "specialization"]
        )

    async def execute(self, patient_id: str, specialization: str, **kwargs) -> Dict[str, Any]:
        """Schedule an appointment for a patient"""
        try:
            # Get available slots from backend
            slots_response = requests.get(
                f"{settings.BACKEND_URL}/api/slots?specialization={specialization}",
                timeout=10
            ).json()

            if not slots_response.get("success"):
                return {
                    "success": False,
                    "message": "No available slots for this specialization"
                }

            slots = slots_response.get("data", [])
            if not slots:
                return {
                    "success": False,
                    "message": "No slots available",
                    "slots": []
                }

            # Auto-book first available slot
            first_slot = slots[0]
            booking_response = requests.post(
                f"{settings.BACKEND_URL}/api/appointments",
                json={
                    "patient_id": patient_id,
                    "doctor_id": first_slot["doctor_id"],
                    "slot": first_slot["slot"]
                },
                timeout=10
            ).json()

            if booking_response.get("success"):
                appointment = booking_response.get("data", {})
                return {
                    "success": True,
                    "appointment": appointment,
                    "message": f"Appointment booked with {first_slot['doctor_name']}"
                }
            else:
                return {
                    "success": False,
                    "message": "Could not complete booking",
                    "available_slots": slots
                }
        except Exception as e:
            logger.error(f"Appointment scheduling error: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

class PatientSummaryTool(Tool):
    """Tool for retrieving patient medical summary"""

    def __init__(self):
        super().__init__(
            name="patient_summary",
            description="Get patient medical summary with records and appointments",
            required_params=["patient_id"]
        )

    async def execute(self, patient_id: str, **kwargs) -> Dict[str, Any]:
        """Get patient summary from backend"""
        try:
            response = requests.get(
                f"{settings.BACKEND_URL}/api/patients/{patient_id}/summary",
                timeout=10
            ).json()

            if response.get("success"):
                return response.get("data", {})
            else:
                return {
                    "success": False,
                    "message": "Patient not found"
                }
        except Exception as e:
            logger.error(f"Patient summary error: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

class FollowupReminderTool(Tool):
    """Tool for creating follow-up reminders"""

    def __init__(self):
        super().__init__(
            name="followup_reminder",
            description="Create a follow-up reminder for a patient",
            required_params=["patient_id", "notes"]
        )

    async def execute(self, patient_id: str, notes: str, **kwargs) -> Dict[str, Any]:
        """Create a follow-up record"""
        try:
            response = requests.post(
                f"{settings.BACKEND_URL}/api/followups",
                json={"patient_id": patient_id, "notes": notes},
                timeout=10
            ).json()

            if response.get("success"):
                return {
                    "success": True,
                    "followup": response.get("data", {}),
                    "message": "Follow-up reminder created successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Could not create follow-up"
                }
        except Exception as e:
            logger.error(f"Followup creation error: {e}")
            return {
                "success": False,
                "message": f"Error: {str(e)}"
            }

# Register all tools
def register_tools(registry):
    """Register all healthcare tools"""
    registry.register(SymptomCheckerTool())
    registry.register(ScheduleAppointmentTool())
    registry.register(PatientSummaryTool())
    registry.register(FollowupReminderTool())
