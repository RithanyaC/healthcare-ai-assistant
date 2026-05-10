"""Agent framework and base agent class"""
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class Intent(str, Enum):
    """User message intents"""
    SYMPTOM_CHECK = "symptom_check"
    APPOINTMENT_SCHEDULING = "appointment_scheduling"
    PATIENT_SUMMARY = "patient_summary"
    FOLLOWUP = "followup"
    GENERAL = "general"

class Agent(ABC):
    """Base class for all healthcare agents"""

    def __init__(self, name: str, description: str, intents: List[Intent]):
        self.name = name
        self.description = description
        self.intents = intents

    @abstractmethod
    async def process(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a message and return agent response
        Returns: {
            "response": str,
            "agent": str,
            "action": str,
            "data": Dict,
            "logs": List[Dict]
        }
        """
        pass

    async def can_handle(self, intent: Intent) -> bool:
        """Check if this agent can handle the intent"""
        return intent in self.intents

class IntentDetector:
    """Detect user intent from natural language"""

    @staticmethod
    def detect_intent(message: str) -> Intent:
        """Detect the intent from a user message"""
        msg_lower = message.lower()

        # Symptom checking intent
        symptom_keywords = ["symptom", "pain", "hurt", "ache", "sick", "ill", "feel", "condition", "disease"]
        if any(kw in msg_lower for kw in symptom_keywords):
            return Intent.SYMPTOM_CHECK

        # Appointment scheduling intent
        schedule_keywords = ["book", "appointment", "schedule", "doctor", "visit", "slot", "when", "available"]
        if any(kw in msg_lower for kw in schedule_keywords):
            return Intent.APPOINTMENT_SCHEDULING

        # Patient summary intent
        summary_keywords = ["summary", "history", "record", "medical", "previous", "past", "show my"]
        if any(kw in msg_lower for kw in summary_keywords):
            return Intent.PATIENT_SUMMARY

        # Followup intent
        followup_keywords = ["follow up", "reminder", "follow-up", "check", "remind"]
        if any(kw in msg_lower for kw in followup_keywords):
            return Intent.FOLLOWUP

        return Intent.GENERAL

class AgentRouter:
    """Route messages to appropriate agents"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}

    def register_agent(self, agent: Agent):
        """Register an agent"""
        self.agents[agent.name] = agent
        logger.info(f"Agent registered: {agent.name}")

    async def route_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Route message to appropriate agent"""
        intent = IntentDetector.detect_intent(message)

        # Find agent that can handle this intent
        for agent_name, agent in self.agents.items():
            if await agent.can_handle(intent):
                logger.info(f"Routing to agent: {agent_name} (intent: {intent})")
                return await agent.process(message, context)

        # Fallback to general response
        return {
            "response": "I can help you with symptom checking, booking appointments, viewing your medical summary, or setting follow-ups. What do you need?",
            "agent": "router",
            "action": "help_menu",
            "data": {"intent": intent},
            "logs": []
        }

# Global router instance
agent_router = AgentRouter()
