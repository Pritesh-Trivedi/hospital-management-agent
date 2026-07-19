from utils.patient_utils import save_patient

def database_node(state):

    patient_id = save_patient(state)

    state["patient_id"] = patient_id

    print("Patient saved with ID:", patient_id)

    state["steps"].append(
        f"Database: patient record saved with ID {patient_id}"
    )

    return state