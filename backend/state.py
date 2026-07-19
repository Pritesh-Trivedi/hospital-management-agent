from typing import TypedDict, List, Optional

class HospitalState(TypedDict):

    patient_name:str
    email: Optional[str]
    age:int
    symptoms:str

    ward:str
    priority:str

    assigned_doctor:str

    reasoning:str

    status:str

    next_slot:str
    slot_minutes:int

    patient_id:str

    notification_id:str
    email_sent: Optional[bool]
    email_status: Optional[str]

    steps: List[str]

    # Phase 1: location + multi-hospital selection
    patient_latitude: Optional[float]
    patient_longitude: Optional[float]

    hospital_id: str
    hospital_name: str
    hospital_address: str
    hospital_latitude: float
    hospital_longitude: float
    hospital_distance_km: float
    hospital_reasoning: str

    # Phase 3: bed allocation
    admission_required: bool
    admission_reasoning: str
    bed_reserved: bool

    # Phase 4: ambulance recommendation + guidance
    emergency_level: str
    ambulance_recommended: bool
    ambulance_reasoning: str
    guidance: str

    # Phase 5: appointment booking
    appointment_id: str
    token_number: str
    consultation_room: str

    # Phase 6: queue management
    queue_position: int
    estimated_wait_minutes: int