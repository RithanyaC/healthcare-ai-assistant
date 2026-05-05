from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json

app = FastAPI()

BACKEND_URL = "http://localhost:8000"

def success_response(data): return {"success": True, "data": data, "error": None}
def error_response(code, message): return {"success": False, "data": None, "error": {"code": code, "message": message}}

class SymptomRequest(BaseModel):
    symptoms: str
@app.post("/tools/symptom_check")
def symptom_check(req: SymptomRequest):
    symptoms = req.symptoms.lower()

    # 🔴 HIGH RISK
    if any(word in symptoms for word in ["chest pain", "shortness of breath", "breathing difficulty", "heart pain"]):
        risk_level = "High"
        specialist = "Cardiology / Emergency Care"
        assessment = "Symptoms may indicate a serious heart or lung condition. Seek immediate medical attention."

    elif any(word in symptoms for word in ["stroke", "paralysis", "seizure", "unconscious"]):
        risk_level = "High"
        specialist = "Neurology / Emergency Care"
        assessment = "Possible neurological emergency. Immediate hospital visit is required."

    # 🟡 MEDIUM RISK
    elif any(word in symptoms for word in ["high fever", "persistent cough", "infection", "vomiting", "diarrhea"]):
        risk_level = "Medium"
        specialist = "General Physician"
        assessment = "Symptoms suggest a possible infection. Consult a doctor within 24 hours."

    elif any(word in symptoms for word in ["stomach pain", "abdominal pain", "indigestion", "gas"]):
        risk_level = "Medium"
        specialist = "Gastroenterologist"
        assessment = "Digestive issue suspected. Avoid heavy food and consult a specialist if it continues."

    # 🟢 LOW RISK
    elif any(word in symptoms for word in ["headache", "cold", "mild fever", "fatigue", "tired"]):
        risk_level = "Low"
        specialist = "General Physician"
        assessment = "Likely a minor illness. Rest, hydrate, and monitor symptoms."

    # 🟣 DEFAULT
    else:
        risk_level = "Medium"
        specialist = "General Physician"
        assessment = "Symptoms are unclear. A general consultation is recommended for proper diagnosis."

    return success_response({
        "assessment": assessment,
        "risk_level": risk_level,
        "recommended_specialist": specialist
    })

class ScheduleRequest(BaseModel):
    patient_id: str
    specialization: str

@app.post("/tools/schedule_appointment")
def schedule_appointment(req: ScheduleRequest):
    # Call backend to find slots
    slots_resp = requests.get(f"{BACKEND_URL}/api/slots?specialization={req.specialization}").json()
    if not slots_resp.get("success"):
        return error_response("SLOT_FETCH_FAILED", "Failed to fetch slots")

    slots = slots_resp["data"]
    if not slots:
        return error_response("NO_SLOTS", "No slots available for this specialization")

    # Book the first available slot
    slot_to_book = slots[0]
    book_resp = requests.post(f"{BACKEND_URL}/api/appointments", json={
        "patient_id": req.patient_id,
        "doctor_id": slot_to_book["doctor_id"],
        "slot": slot_to_book["slot"]
    }).json()

    if not book_resp.get("success"):
        return error_response("BOOKING_ERROR", book_resp.get("error", {}).get("message", "Failed to book"))

    return success_response({
        "appointment": book_resp["data"]
    })

class PatientSummaryRequest(BaseModel):
    patient_id: str

@app.post("/tools/patient_summary")
def patient_summary(req: PatientSummaryRequest):
    resp = requests.get(f"{BACKEND_URL}/api/patients/{req.patient_id}/summary").json()
    if resp.get("success"):
        return success_response({"summary": resp["data"]})
    return error_response("SUMMARY_FAILED", "Failed to get patient summary")

class FollowupRequest(BaseModel):
    patient_id: str
    notes: str

@app.post("/tools/followup_reminder")
def followup_reminder(req: FollowupRequest):
    resp = requests.post(f"{BACKEND_URL}/api/followups", json={"patient_id": req.patient_id, "notes": req.notes}).json()
    if resp.get("success"):
        return success_response({"followup": resp["data"]})
    return error_response("FOLLOWUP_FAILED", "Failed to create followup")

@app.post("/tools/predict_waittime")
def predict_waittime():
    return success_response({"waittime_minutes": 15})

class UrgentRequest(BaseModel):
    patient_id: str

@app.post("/tools/flag_urgent")
def flag_urgent(req: UrgentRequest):
    return success_response({"status": "Patient flagged as urgent", "patient_id": req.patient_id})

@app.get("/tools/get_analytics")
def get_analytics():
    return success_response({"total_appointments": 10, "average_wait_time": 15})

class EhrRequest(BaseModel):
    patient_id: str
    notes: str

@app.post("/tools/update_ehr_notes")
def update_ehr_notes(req: EhrRequest):
    resp = requests.post(f"{BACKEND_URL}/api/followups", json={"patient_id": req.patient_id, "notes": req.notes}).json()
    if resp.get("success"):
        return success_response({"record": resp["data"]})
    return error_response("EHR_UPDATE_FAILED", "Failed to update EHR notes")
