from utils.queue_utils import add_to_queue

def queue_management_node(state):

    queue_info = add_to_queue(state)

    state["queue_position"] = queue_info["queue_position"]
    state["estimated_wait_minutes"] = queue_info["estimated_wait"]

    print("Queue Position:", state["queue_position"], "Estimated Wait:", state["estimated_wait_minutes"], "min")

    state["steps"].append(
        f"Queue Management: queue position {state['queue_position']} at {state['hospital_name']}, "
        f"estimated wait {state['estimated_wait_minutes']} minutes"
    )

    return state