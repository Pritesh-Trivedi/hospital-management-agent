import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _data_path(filename):
    return DATA_DIR / filename


def _normalize_ward(ward):
    return str(ward or "").strip().lower().replace(" ", "_").replace("-", "_")


def _get_next_slot(queue_position, slot_minutes):
    now = datetime.now()
    slot_time = now + timedelta(minutes=queue_position * slot_minutes)

    remainder = slot_time.minute % 5
    if remainder != 0:
        slot_time += timedelta(minutes=5 - remainder)

    slot_time = slot_time.replace(second=0, microsecond=0)
    return slot_time.strftime("%H:%M")


def assign_doctor(ward):

    ward = _normalize_ward(ward)

    doctors = pd.read_csv(_data_path("doctors.csv"))

    available = doctors[
        (doctors["ward"] == ward) &
        (doctors["status"] == "active") &
        (doctors["current_patients"] < doctors["max_patients"])
    ]

    if available.empty:
        return None

    selected = available.sort_values("current_patients").iloc[0]

    slot_minutes = int(selected["slot_minutes"])
    queue_position = int(selected["current_patients"])
    next_slot = _get_next_slot(queue_position, slot_minutes)

    doctors.loc[
        doctors["doctor_id"] == selected["doctor_id"],
        "current_patients"
    ] += 1

    doctors.to_csv(_data_path("doctors.csv"), index=False)

    return {
        "doctor_name": selected["doctor_name"],
        "next_slot": next_slot,
        "slot_minutes": slot_minutes
    }


def get_available_doctors(ward, current_doctor=None):

    if not ward:
        return []

    ward = _normalize_ward(ward)

    doctors = pd.read_csv(_data_path("doctors.csv"))

    mask = (
        (doctors["ward"] == ward) &
        (doctors["status"] == "active") &
        (doctors["current_patients"] < doctors["max_patients"])
    )

    if current_doctor:
        mask &= (doctors["doctor_name"] != current_doctor)

    available = doctors[mask]

    doctor_list = []

    for _, doctor in available.iterrows():
        slot_minutes = int(doctor["slot_minutes"])
        queue_position = int(doctor["current_patients"])

        doctor_list.append({
            "doctor_name": doctor["doctor_name"],
            "next_slot": _get_next_slot(queue_position, slot_minutes),
            "slot_minutes": slot_minutes,
            "current_patients": int(doctor["current_patients"])
        })

    return doctor_list


def change_doctor(patient_id, new_doctor):

    doctors = pd.read_csv(_data_path("doctors.csv"))
    patients = pd.read_csv(_data_path("patients.csv"))

    patient = patients[patients["patient_id"] == patient_id]
    if patient.empty:
        return {"error": "Patient not found"}

    patient_row = patient.iloc[0]
    old_doctor = patient_row["doctor"]

    new_doctor_row = doctors[doctors["doctor_name"] == new_doctor]
    if new_doctor_row.empty:
        return {"error": "Doctor not found"}

    if old_doctor and old_doctor != new_doctor:
        old_doctor_row = doctors[doctors["doctor_name"] == old_doctor]
        if not old_doctor_row.empty:
            doctors.loc[old_doctor_row.index[0], "current_patients"] -= 1

    new_doctor_index = new_doctor_row.index[0]
    slot_minutes = int(doctors.loc[new_doctor_index, "slot_minutes"])
    queue_position = int(doctors.loc[new_doctor_index, "current_patients"])
    next_slot = _get_next_slot(queue_position, slot_minutes)

    doctors.loc[new_doctor_index, "current_patients"] += 1

    patients.loc[
        patients["patient_id"] == patient_id,
        "doctor"
    ] = new_doctor

    doctors.to_csv(_data_path("doctors.csv"), index=False)
    patients.to_csv(_data_path("patients.csv"), index=False)

    return {
        "doctor": new_doctor,
        "next_slot": next_slot,
        "slot_minutes": slot_minutes
    }