import pandas as pd

WARD_ROOM_PREFIX = {
    "emergency": "ER",
    "general": "GEN",
    "mental_health": "MH",
}


def generate_appointment_id():

    appointments = pd.read_csv("data/appointments.csv")

    if len(appointments) == 0:
        return "A1001"

    last_id = appointments.iloc[-1]["appointment_id"]
    number = int(last_id[1:])

    return f"A{number + 1}"


def book_appointment(state):

    appointments = pd.read_csv("data/appointments.csv")

    appointment_id = generate_appointment_id()

    ward_key = state["ward"].strip().lower().replace(" ", "_")
    prefix = WARD_ROOM_PREFIX.get(ward_key, "GEN")

    # How many appointments this doctor already has today decides the
    # token number and the consultation room, so both increment in a
    # simple, deterministic, demo-safe way.
    doctor_appointments = appointments[appointments["doctor"] == state["assigned_doctor"]]
    token_number = f"T{len(doctor_appointments) + 1:03d}"
    consultation_room = f"{prefix}-{(len(doctor_appointments) % 5) + 1}"

    new_appointment = {
        "appointment_id": appointment_id,
        "patient_id": state["patient_id"],
        "doctor": state["assigned_doctor"],
        "hospital": state["hospital_name"],
        "appointment_time": state["next_slot"],
        "token_number": token_number,
        "consultation_room": consultation_room,
    }

    appointments = pd.concat(
        [appointments, pd.DataFrame([new_appointment])],
        ignore_index=True
    )

    appointments.to_csv("data/appointments.csv", index=False)

    return {
        "appointment_id": appointment_id,
        "token_number": token_number,
        "consultation_room": consultation_room,
    }