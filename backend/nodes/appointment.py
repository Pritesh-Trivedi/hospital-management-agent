from utils.appointment_utils import book_appointment

def appointment_node(state):

    appointment = book_appointment(state)

    state["appointment_id"] = appointment["appointment_id"]
    state["token_number"] = appointment["token_number"]
    state["consultation_room"] = appointment["consultation_room"]

    print("Appointment Booked:", appointment["appointment_id"], "Token:", appointment["token_number"])

    state["steps"].append(
        f"Appointment Booking: booked {appointment['appointment_id']}, token {appointment['token_number']}, "
        f"room {appointment['consultation_room']}, at {state['next_slot']}"
    )

    return state