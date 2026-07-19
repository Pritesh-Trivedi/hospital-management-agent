def intake_node(state):
    print("Patient information received")

    state["steps"].append(
        f"Intake: received patient {state['patient_name']}, age {state['age']}"
    )

    return state