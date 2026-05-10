"""
Healthcare AI Assistant - MCP (Multi-agent Convergence Platform) Server
Version 2.0: Agent-based architecture with modular tools
Tool orchestration layer for AI-driven healthcare consultations
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from app.config.settings import settings
from app.tools.registry import tool_registry
from app.tools.healthcare_tools import register_tools
from app.agents.base import agent_router
from app.agents.healthcare_agents import register_agents

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Healthcare AI MCP Server",
    description="Agent orchestration platform for healthcare AI",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[str] = "p1"
    context: Optional[str] = "healthcare_consultation"

# Initialize on startup
@app.on_event("startup")
async def startup():
    """Initialize tools and agents on startup"""
    logger.info("Starting MCP Server v2.0")

    # Register all tools
    register_tools(tool_registry)
    logger.info(f"Registered {len(tool_registry.tools)} tools")

    # Register all agents
    register_agents(agent_router)
    logger.info(f"Registered agents: Triage, Scheduling, Summary, Followup")

# Routes - Legacy tool endpoints (backward compatibility)
@app.post("/tools/symptom_check")
async def symptom_check(request: ChatRequest):
    """Legacy endpoint for symptom checking"""
    return await tool_registry.execute_tool("symptom_check", symptoms=request.message)

@app.post("/tools/schedule_appointment")
async def schedule_appointment(request: ChatRequest):
    """Legacy endpoint for scheduling"""
    return await tool_registry.execute_tool(
        "schedule_appointment",
        patient_id=request.patient_id,
        specialization="General Physician"
    )

@app.post("/tools/patient_summary")
async def patient_summary(request: ChatRequest):
    """Legacy endpoint for patient summary"""
    return await tool_registry.execute_tool("patient_summary", patient_id=request.patient_id)

@app.post("/tools/followup_reminder")
async def followup_reminder(request: ChatRequest):
    """Legacy endpoint for follow-ups"""
    return await tool_registry.execute_tool(
        "followup_reminder",
        patient_id=request.patient_id,
        notes=request.message
    )
# Backward compatibility endpoint for frontend
@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Compatibility chat endpoint.
    Redirects frontend chat requests to orchestration layer.
    """

    result = await orchestrate(request)

    return {
        "success": result.get("success", True),
        "response": result.get("response", ""),
        "agent": result.get("agent", ""),
        "action": result.get("action", ""),
        "data": result.get("data", {}),
        "logs": result.get("logs", [])
    }

# New agent-based orchestration endpoint
@app.post("/orchestrate")
async def orchestrate(request: ChatRequest):
    """
    Main orchestration endpoint.
    Routes message to appropriate agent based on intent.
    Maintains backward compatibility with original API.
    """
    try:
        context = {
            "patient_id": request.patient_id,
            "context": request.context
        }

        result = await agent_router.route_message(request.message, context)

        return {
            "success": True,
            "response": result.get("response", ""),
            "agent": result.get("agent", "unknown"),
            "action": result.get("action", ""),
            "data": result.get("data", {}),
            "logs": result.get("logs", [])
        }
    except Exception as e:
        logger.error(f"Orchestration error: {e}")
        return {
            "success": False,
            "error": str(e),
            "response": "An error occurred while processing your request."
        }

# List available tools
@app.get("/tools")
async def list_tools():
    """List all available tools and their descriptions"""
    return {
        "success": True,
        "tools": tool_registry.list_tools(),
        "count": len(tool_registry.tools)
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "success": True,
        "status": "healthy",
        "service": "MCP Server",
        "version": "2.0.0",
        "tools": len(tool_registry.tools),
        "agents": len(agent_router.agents)
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "name": "Healthcare AI MCP Server",
        "version": "2.0.0",
        "description": "Agent orchestration platform for healthcare AI",
        "status": "running",
        "endpoints": {
            "orchestrate": "/orchestrate (POST) - Main agent routing",
            "tools": "/tools (GET) - List available tools",
            "legacy_tools": {
                "symptom_check": "/tools/symptom_check (POST)",
                "schedule": "/tools/schedule_appointment (POST)",
                "summary": "/tools/patient_summary (POST)",
                "followup": "/tools/followup_reminder (POST)"
            },
            "health": "/health (GET)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
