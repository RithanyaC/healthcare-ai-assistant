import json
import os
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")

def read_json(filename):
    with open(os.path.join(DATA_DIR, filename), "r") as f:
        return json.load(f)

def write_json(filename, data):
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=2)

def success_response(data): return {"success": True, "data": data, "error": None}
def error_response(code, message): return {"success": False, "data": None, "error": {"code": code, "message": message}}

# --- SERVICES ---
def get_patient_summary(patient_id: str):
    patients = read_json("patients.json")
    patient = next((p for p in patients if p["id"] == patient_id), None)
    if not patient:
        return None
    records = [r for r in read_json("records.json") if r["patient_id"] == patient_id]
    appointments = [a for a in read_json("appointments.json") if a["patient_id"] == patient_id]
    return {
        "patient": patient,
        "recent_records": records[-5:],
        "upcoming_appointments": [a for a in appointments if a["status"] != "completed"]
    }

def find_available_slots(specialization: str):
    doctors = read_json("doctors.json")
    available_slots = []
    for doctor in doctors:
        if doctor["specialization"].lower() == specialization.lower():
            for slot in doctor["available_slots"]:
                available_slots.append({"doctor_id": doctor["id"], "doctor_name": doctor["name"], "slot": slot})
    return available_slots

def book_appointment(patient_id: str, doctor_id: str, slot: str):
    patients = read_json("patients.json")
    if not any(p["id"] == patient_id for p in patients):
        raise ValueError("Patient not found")
        
    doctors = read_json("doctors.json")
    doctor = next((d for d in doctors if d["id"] == doctor_id), None)
    if not doctor:
        raise ValueError("Doctor not found")
        
    if slot not in doctor["available_slots"]:
        raise ValueError("Slot not available")
        
    appointments = read_json("appointments.json")
    for appt in appointments:
        if appt["doctor_id"] == doctor_id and appt["slot"] == slot:
            raise ValueError("Slot already booked")
            
    new_appt = {
        "id": f"a{len(appointments)+1}",
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "slot": slot,
        "status": "scheduled"
    }
    appointments.append(new_appt)
    write_json("appointments.json", appointments)
    
    doctor["available_slots"].remove(slot)
    write_json("doctors.json", doctors)
    return new_appt

def get_patient_record(patient_id: str):
    records = read_json("records.json")
    return [r for r in records if r["patient_id"] == patient_id]

def create_followup(patient_id: str, notes: str):
    records = read_json("records.json")
    new_record = {
        "id": f"r{len(records)+1}",
        "patient_id": patient_id,
        "date": datetime.utcnow().isoformat() + "Z",
        "notes": notes,
        "type": "Follow-up"
    }
    records.append(new_record)
    write_json("records.json", records)
    return new_record

# --- APIs ---
@app.get("/api/patients/{patient_id}/summary")
def api_patient_summary(patient_id: str):
    summary = get_patient_summary(patient_id)
    if summary: return success_response(summary)
    return error_response("NOT_FOUND", "Patient not found")

@app.get("/api/slots")
def api_find_slots(specialization: str):
    slots = find_available_slots(specialization)
    return success_response(slots)

class BookingRequest(BaseModel):
    patient_id: str
    doctor_id: str
    slot: str

@app.post("/api/appointments")
def api_book_appointment(req: BookingRequest):
    try:
        appt = book_appointment(req.patient_id, req.doctor_id, req.slot)
        return success_response(appt)
    except ValueError as e:
        return error_response("BOOKING_FAILED", str(e))

class FollowupRequest(BaseModel):
    patient_id: str
    notes: str

@app.post("/api/followups")
def api_create_followup(req: FollowupRequest):
    try:
        record = create_followup(req.patient_id, req.notes)
        return success_response(record)
    except Exception as e:
        return error_response("SERVER_ERROR", str(e))

# --- ORCHESTRATOR & AGENTS ---
MCP_URL = "http://localhost:8001"

class ChatRequest(BaseModel):
    message: str
    patient_id: Optional[str] = "p1"

def a2a_message(from_agent, to_agent, action, payload):
    return {
        "protocol": "COIN",
        "from": from_agent,
        "to": to_agent,
        "action": action,
        "session_id": "session_123",
        "payload": payload
    }

@app.post("/chat")
def chat_orchestrator(req: ChatRequest):
    msg = req.message.lower()
    
    if "pain" in msg or "symptom" in msg or "hurt" in msg:
        intent = "triage"
    elif "book" in msg or "appointment" in msg or "schedule" in msg or "doctor" in msg or "tomorrow" in msg:
        intent = "scheduling"
    elif "summary" in msg or "history" in msg or "record" in msg:
        intent = "summary"
    elif "follow up" in msg or "remind" in msg:
        intent = "followup"
    else:
        return success_response({"reply": "I can help you check symptoms, book an appointment, view your medical summary, or schedule a follow-up. How can I assist?"})

    reply_text = ""
    agent_logs = []
    
    try:
        if intent == "triage":
            agent_logs.append(a2a_message("orchestrator", "triage_agent", "assess_symptoms", {"message": msg}))
            resp = requests.post(f"{MCP_URL}/tools/symptom_check", json={"symptoms": msg}).json()
            if resp.get("success"):
                data = resp["data"]
                reply_text = f"Triage Assessment: {data['assessment']}. Risk Level: {data['risk_level']}. Recommended Specialist: {data['recommended_specialist']}."
                agent_logs.append(a2a_message("triage_agent", "orchestrator", "assessment_complete", data))
            else:
                reply_text = "I couldn't assess those symptoms."
                
        elif intent == "scheduling":
            agent_logs.append(a2a_message("orchestrator", "scheduling_agent", "find_slots", {"specialization": "General Practice"}))
            resp = requests.post(f"{MCP_URL}/tools/schedule_appointment", json={"specialization": "General Practice", "patient_id": req.patient_id}).json()
            if resp.get("success"):
                data = resp["data"]
                if "appointment" in data:
                    reply_text = f"Appointment booked successfully! ID: {data['appointment']['id']} with doctor {data['appointment']['doctor_id']} at {data['appointment']['slot']}."
                else:
                    reply_text = f"Available slots for General Practice: " + ", ".join([f"{s['slot']} with {s['doctor_name']}" for s in data.get("slots", [])])
                agent_logs.append(a2a_message("scheduling_agent", "orchestrator", "scheduling_complete", data))
            else:
                reply_text = "Could not schedule appointment."
                
        elif intent == "summary":
            agent_logs.append(a2a_message("orchestrator", "summary_agent", "get_summary", {"patient_id": req.patient_id}))
            resp = requests.post(f"{MCP_URL}/tools/patient_summary", json={"patient_id": req.patient_id}).json()
            if resp.get("success"):
                data = resp["data"]["summary"]
                reply_text = f"Here is your summary: {data['patient']['name']}, Age: {data['patient']['age']}. "
                reply_text += f"You have {len(data['recent_records'])} recent records and {len(data['upcoming_appointments'])} upcoming appointments."
                agent_logs.append(a2a_message("summary_agent", "orchestrator", "summary_complete", data))
            else:
                reply_text = "Could not retrieve summary."
                
        elif intent == "followup":
            agent_logs.append(a2a_message("orchestrator", "followup_agent", "create_followup", {"patient_id": req.patient_id, "notes": "Follow up requested by user"}))
            resp = requests.post(f"{MCP_URL}/tools/followup_reminder", json={"patient_id": req.patient_id, "notes": "Follow-up requested."}).json()
            if resp.get("success"):
                reply_text = "I have created a follow-up reminder for you."
                agent_logs.append(a2a_message("followup_agent", "orchestrator", "followup_complete", {"status": "created"}))
            else:
                reply_text = "Could not create follow-up."
    except Exception as e:
        return error_response("MCP_ERROR", f"Error communicating with MCP server: {str(e)}")
        
    return success_response({
        "reply": reply_text,
        "logs": agent_logs,
        "intent": intent
    })

@app.post("/chat/stream")
async def chat_stream(req: Request):
    # Basic SSE streaming wrapper around the normal orchestrator
    data = await req.json()
    chat_req = ChatRequest(**data)
    
    async def event_generator():
        yield f"data: {json.dumps({'event': 'started', 'message': 'Processing request...'})}\n\n"
        await asyncio.sleep(0.5)
        
        response = chat_orchestrator(chat_req)
        
        yield f"data: {json.dumps({'event': 'completed', 'response': response})}\n\n"
        
    return StreamingResponse(event_generator(), media_type="text/event-stream")
