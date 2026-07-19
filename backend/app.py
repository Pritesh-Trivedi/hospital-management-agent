from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from graph import graph
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(override=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def home():
    return {"message":"Hospital Agent Running"}


class PatientRequest(BaseModel):
    patient_name: str
    email: Optional[str] = None
    age: int
    symptoms: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@app.post("/triage")
def triage_patient(patient: PatientRequest):

    state = {
        "patient_name": patient.patient_name,
        "email": patient.email,
        "email_sent": False,
        "email_status": "",
        "age": patient.age,
        "symptoms": patient.symptoms,
        "ward": "",
        "priority": "",
        "assigned_doctor": "",
        "reasoning": "",
        "status": "",
        "next_slot": "",
        "slot_minutes": 0,
        "patient_id": "",
        "notification_id": "",
        "steps": [],
        "patient_latitude": patient.latitude,
        "patient_longitude": patient.longitude,
        "hospital_id": "",
        "hospital_name": "",
        "hospital_address": "",
        "hospital_latitude": 0.0,
        "hospital_longitude": 0.0,
        "hospital_distance_km": 0.0,
        "hospital_reasoning": "",
        "admission_required": False,
        "admission_reasoning": "",
        "bed_reserved": False,
        "emergency_level": "",
        "ambulance_recommended": False,
        "ambulance_reasoning": "",
        "guidance": "",
        "appointment_id": "",
        "token_number": "",
        "consultation_room": "",
        "queue_position": 0,
        "estimated_wait_minutes": 0
    }

    result = graph.invoke(state)

    return result