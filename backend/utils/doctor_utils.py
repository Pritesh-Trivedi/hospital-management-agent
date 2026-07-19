import pandas as pd
from datetime import datetime, timedelta

def assign_doctor(ward):

    ward = ward.lower().replace(" ", "_")

    doctors = pd.read_csv("data/doctors.csv")

    available = doctors[
        (doctors["ward"] == ward) &
        (doctors["status"] == "active") &
        (doctors["current_patients"] < doctors["max_patients"])
    ]

    if available.empty:
        return None

    selected = available.sort_values("current_patients").iloc[0]

    slot_minutes = int(selected["slot_minutes"])
    queue_position = int(selected["current_patients"])  # patients already ahead in queue

    # Real next available slot = now + (however many patients are already
    # queued for this doctor) * (this doctor's slot length), rounded up to
    # the next 5-minute mark so it looks like a real clinic schedule.
    now = datetime.now()
    minutes_until_slot = queue_position * slot_minutes
    raw_slot_time = now + timedelta(minutes=minutes_until_slot)

    remainder = raw_slot_time.minute % 5
    if remainder != 0:
        raw_slot_time += timedelta(minutes=(5 - remainder))
    raw_slot_time = raw_slot_time.replace(second=0, microsecond=0)

    next_slot = raw_slot_time.strftime("%H:%M")

    doctors.loc[
        doctors["doctor_id"] == selected["doctor_id"],
        "current_patients"
    ] += 1

    doctors.to_csv("data/doctors.csv", index=False)

    return {
        "doctor_name": selected["doctor_name"],
        "next_slot": next_slot,
        "slot_minutes": slot_minutes
    }