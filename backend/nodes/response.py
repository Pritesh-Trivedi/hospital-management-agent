from utils.notification_utils import create_notification

def response_node(state):

    print("Preparing final response")

    state["steps"].append(
        f"Response: triage complete — {state['status']} for {state['patient_name']} in {state['ward']} ward"
    )

    return state