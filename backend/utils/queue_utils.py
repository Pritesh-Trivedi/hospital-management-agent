import pandas as pd
from config import DATA_DIR


def add_to_queue(state):

    queue = pd.read_csv(DATA_DIR / "queue.csv")

    hospital_queue = queue[queue["hospital_id"] == state["hospital_id"]]
    queue_position = len(hospital_queue) + 1

    # Estimated wait = how many patients are ahead of this one at this
    # hospital, times this doctor's average consultation length.
    estimated_wait = queue_position * state["slot_minutes"]

    new_entry = {
        "hospital_id": state["hospital_id"],
        "patient_id": state["patient_id"],
        "queue_position": queue_position,
        "estimated_wait": estimated_wait,
        "token_number": state["token_number"],
    }

    queue = pd.concat(
        [queue, pd.DataFrame([new_entry])],
        ignore_index=True
    )

    queue.to_csv(DATA_DIR / "queue.csv", index=False)

    return {
        "queue_position": queue_position,
        "estimated_wait": estimated_wait,
    }