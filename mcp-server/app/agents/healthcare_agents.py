"""Specific healthcare agents"""
from app.agents.base import Agent, Intent
from app.tools.registry import tool_registry
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class TriageAgent(Agent):
    """Agent for symptom triage and assessment"""

    def __init__(self):
        super().__init__(
            name="triage_agent",
            description="Assess patient symptoms and provide triage recommendations",
            intents=[Intent.SYMPTOM_CHECK]
        )

    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process symptom check request"""
        logs = []

        # Log agent action
        logs.append({
            "protocol": "COIN",
            "from": "router",
            "to": self.name,
            "action": "assess_symptoms",
            "payload": {"message": message}
        })

        # Execute symptom checker tool
        tool_result = await tool_registry.execute_tool("symptom_check", symptoms=message)

        logs.append({
            "protocol": "COIN",
            "from": self.name,
            "to": "backend",
            "action": "symptom_analysis_complete",
            "payload": tool_result.get("data", {})
        })

        if tool_result.get("success"):
            data = tool_result.get("data", {})
            response = (
                f"🏥 **Triage Assessment**\n\n"
                f"**Symptoms:** {data.get('symptoms_reported', '')}\n"
                f"**Risk Level:** {data.get('risk_level', 'Unknown')}\n"
                f"**Assessment:** {data.get('assessment', '')}\n"
                f"**Recommended Specialist:** {data.get('recommended_specialist', 'General Physician')}"
            )
        else:
            response = "I encountered an error analyzing your symptoms. Please try again."
            data = {}

        return {
            "response": response,
            "agent": self.name,
            "action": "symptom_assessment",
            "data": data,
            "logs": logs
        }

class SchedulingAgent(Agent):
    """Agent for appointment scheduling"""

    def __init__(self):
        super().__init__(
            name="scheduling_agent",
            description="Help patients find and book appointments",
            intents=[Intent.APPOINTMENT_SCHEDULING]
        )

    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process appointment scheduling request"""
        logs = []
        patient_id = context.get("patient_id", "p1")

        logs.append({
            "protocol": "COIN",
            "from": "router",
            "to": self.name,
            "action": "schedule_appointment",
            "payload": {"message": message, "patient_id": patient_id}
        })

        # Determine specialization from message or use default
        specialization = self._extract_specialization(message) or "General Physician"

        # Execute scheduling tool
        tool_result = await tool_registry.execute_tool(
            "schedule_appointment",
            patient_id=patient_id,
            specialization=specialization
        )

        logs.append({
            "protocol": "COIN",
            "from": self.name,
            "to": "backend",
            "action": "scheduling_complete",
            "payload": tool_result
        })

        if tool_result.get("success"):
            data = tool_result.get("data", {})
            appointment = data.get("appointment", {})
            response = (
                f"✅ **Appointment Booked Successfully**\n\n"
                f"**Appointment ID:** {appointment.get('id', 'N/A')}\n"
                f"**Date & Time:** {appointment.get('slot', 'N/A')}\n"
                f"**Doctor:** {appointment.get('doctor_id', 'N/A')}\n"
                f"**Status:** {appointment.get('status', 'Scheduled')}"
            )
        else:
            data = tool_result
            response = f"❌ {tool_result.get('data', {}).get('message', 'Could not schedule appointment')}"

        return {
            "response": response,
            "agent": self.name,
            "action": "appointment_booked",
            "data": data,
            "logs": logs
        }

    def _extract_specialization(self, message: str) -> str:
        """Extract specialization from user message"""
        specializations = ["cardiology", "neurology", "general", "pediatrics", "orthopedics"]
        msg_lower = message.lower()
        for spec in specializations:
            if spec in msg_lower:
                return spec.title()
        return None

class SummaryAgent(Agent):
    """Agent for retrieving patient medical summaries"""

    def __init__(self):
        super().__init__(
            name="summary_agent",
            description="Provide patient medical summaries and history",
            intents=[Intent.PATIENT_SUMMARY]
        )

    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process patient summary request"""
        logs = []
        patient_id = context.get("patient_id", "p1")

        logs.append({
            "protocol": "COIN",
            "from": "router",
            "to": self.name,
            "action": "get_summary",
            "payload": {"patient_id": patient_id}
        })

        tool_result = await tool_registry.execute_tool(
            "patient_summary",
            patient_id=patient_id
        )

        logs.append({
            "protocol": "COIN",
            "from": self.name,
            "to": "backend",
            "action": "summary_retrieved",
            "payload": tool_result
        })

        if tool_result.get("success"):
            data = tool_result.get("data", {})
            patient = data.get("patient", {})
            records = data.get("recent_records", [])
            appointments = data.get("upcoming_appointments", [])

            response = (
                f"📋 **Patient Summary**\n\n"
                f"**Name:** {patient.get('name', 'N/A')}\n"
                f"**Age:** {patient.get('age', 'N/A')}\n"
                f"**Medical History:** {patient.get('medical_history', 'None')}\n"
                f"**Allergies:** {patient.get('allergies', 'None')}\n\n"
                f"**Recent Records:** {len(records)}\n"
                f"**Upcoming Appointments:** {len(appointments)}"
            )
        else:
            data = {}
            response = "Could not retrieve patient summary."

        return {
            "response": response,
            "agent": self.name,
            "action": "summary_provided",
            "data": data,
            "logs": logs
        }

class FollowupAgent(Agent):
    """Agent for managing follow-up reminders"""

    def __init__(self):
        super().__init__(
            name="followup_agent",
            description="Create and manage follow-up reminders",
            intents=[Intent.FOLLOWUP]
        )

    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process follow-up reminder request"""
        logs = []
        patient_id = context.get("patient_id", "p1")

        logs.append({
            "protocol": "COIN",
            "from": "router",
            "to": self.name,
            "action": "create_followup",
            "payload": {"patient_id": patient_id, "message": message}
        })

        tool_result = await tool_registry.execute_tool(
            "followup_reminder",
            patient_id=patient_id,
            notes=message
        )

        logs.append({
            "protocol": "COIN",
            "from": self.name,
            "to": "backend",
            "action": "followup_created",
            "payload": tool_result
        })

        if tool_result.get("success"):
            data = tool_result.get("data", {})
            response = (
                f"⏰ **Follow-up Reminder Created**\n\n"
                f"**Status:** {tool_result.get('data', {}).get('message', 'Created')}\n"
                f"We'll remind you to check in on your health."
            )
        else:
            data = {}
            response = "Could not create follow-up reminder."

        return {
            "response": response,
            "agent": self.name,
            "action": "followup_created",
            "data": data,
            "logs": logs
        }

def register_agents(router):
    """Register all healthcare agents"""
    router.register_agent(TriageAgent())
    router.register_agent(SchedulingAgent())
    router.register_agent(SummaryAgent())
    router.register_agent(FollowupAgent())
