from utils.doctor_utils import assign_doctor

def doctor_node(state):

    ward = state["ward"].strip().lower().replace(" ", "_")

    doctor = assign_doctor(ward)

    if doctor is None:
        state["assigned_doctor"] = "No doctor available"
        state["status"] = "Waiting"
    else:
        state["assigned_doctor"] = doctor["doctor_name"]
        state["status"] = "Doctor Assigned"
        state["next_slot"] = doctor["next_slot"]
        state["slot_minutes"] = int(doctor["slot_minutes"])

    print("Assigned Doctor:", state["assigned_doctor"])

    if state["status"] == "Waiting":
        state["steps"].append(
            f"Doctor Availability: no free doctor in {state['ward']} ward, patient placed on waiting status"
        )
    else:
        state["steps"].append(
            f"Doctor Availability: assigned {state['assigned_doctor']} in {state['ward']} ward, next slot {state['next_slot']}"
        )

    return state