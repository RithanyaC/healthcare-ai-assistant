"""Chat and orchestration routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.base import get_db
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import requests
import logging

router = APIRouter(prefix="/api", tags=["chat"])
logger = logging.getLogger(__name__)

from app.config.settings import settings

class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[str] = "p1"

class AgentLog(BaseModel):
    protocol: str
    from_agent: str
    to_agent: str
    action: str
    payload: Dict[str, Any]

@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    """
    Main chat endpoint for AI agent orchestration.
    Routes message to appropriate agent via MCP server.
    """
    try:
        # Call MCP server for agent orchestration
        mcp_response = requests.post(
            f"{settings.MCP_SERVER_URL}/orchestrate",
            json={
                "message": req.message,
                "patient_id": req.patient_id,
                "context": "healthcare_consultation"
            },
            timeout=30
        )

        if mcp_response.status_code != 200:
            return {
                "success": False,
                "data": None,
                "error": {
                    "code": "ORCHESTRATION_FAILED",
                    "message": "Failed to process message through AI agents"
                }
            }

        agent_response = mcp_response.json()

        return {
            "success": True,
            "data": {
                "reply": agent_response.get("response", ""),
                "agent": agent_response.get("agent", "unknown"),
                "logs": agent_response.get("logs", []),
                "action_taken": agent_response.get("action", None)
            },
            "error": None
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"MCP Server error: {e}")
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "SERVICE_UNAVAILABLE",
                "message": "AI orchestration service is unavailable. Ensure MCP server is running."
            }
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Healthcare AI Backend",
        "version": "2.0.0"
    }
