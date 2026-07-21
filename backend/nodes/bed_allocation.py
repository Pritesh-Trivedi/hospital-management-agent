import pandas as pd

from config import DATA_DIR
from utils.location_utils import haversine_distance_km
from nodes.hospital_selection import score_hospital


def bed_allocation_node(state):

    # admission_required is now decided by nodes/admission.py (LLM-reasoned),
    # this node just acts on it.
    admission_required = state["admission_required"]

    if not admission_required:
        state["bed_reserved"] = False
        state["steps"].append(
            "Bed Allocation: admission not required, skipped"
        )
        return state

    ward = state["ward"].strip().lower().replace(" ", "_")
    beds = pd.read_csv(DATA_DIR / "beds.csv")
    hospitals = pd.read_csv(DATA_DIR / "hospitals.csv")

    current_hospital_id = state["hospital_id"]

    # Build a fallback order: try the currently selected hospital first,
    # then re-rank the remaining hospitals using the same scoring formula
    # from hospital_selection.py, so the fallback choice is still reasoned
    # rather than arbitrary.
    candidate_ids = [current_hospital_id]

    remaining = hospitals[hospitals["hospital_id"] != current_hospital_id].copy()
    if not remaining.empty:
        remaining["distance_km"] = remaining.apply(
            lambda row: haversine_distance_km(
                state["patient_latitude"],
                state["patient_longitude"],
                row["latitude"],
                row["longitude"],
            ),
            axis=1,
        )
        remaining["score"] = remaining.apply(
            lambda row: score_hospital(row["distance_km"], row["rating"], row["queue_length"]),
            axis=1,
        )
        remaining = remaining.sort_values("score", ascending=False)
        candidate_ids += remaining["hospital_id"].tolist()

    for hospital_id in candidate_ids:
        bed_row = beds[(beds["hospital_id"] == hospital_id) & (beds["ward"] == ward)]

        if bed_row.empty:
            continue

        row = bed_row.iloc[0]

        if row["occupied_beds"] < row["total_beds"]:
            beds.loc[
                (beds["hospital_id"] == hospital_id) & (beds["ward"] == ward),
                "occupied_beds"
            ] += 1
            beds.to_csv(DATA_DIR / "beds.csv", index=False)

            if hospital_id != current_hospital_id:
                new_hospital = hospitals[hospitals["hospital_id"] == hospital_id].iloc[0]
                new_distance = haversine_distance_km(
                    state["patient_latitude"],
                    state["patient_longitude"],
                    new_hospital["latitude"],
                    new_hospital["longitude"],
                )

                old_hospital_name = state["hospital_name"]

                state["hospital_id"] = hospital_id
                state["hospital_name"] = new_hospital["hospital_name"]
                state["hospital_address"] = new_hospital["address"]
                state["hospital_latitude"] = float(new_hospital["latitude"])
                state["hospital_longitude"] = float(new_hospital["longitude"])
                state["hospital_distance_km"] = float(new_distance)
                state["hospital_reasoning"] += (
                    f" Reassigned from {old_hospital_name} to {new_hospital['hospital_name']} "
                    f"because no {state['ward']} beds were available there."
                )

                state["steps"].append(
                    f"Bed Allocation: {old_hospital_name} had no available {state['ward']} beds, "
                    f"automatically reassigned to {new_hospital['hospital_name']}"
                )
            else:
                state["steps"].append(
                    f"Bed Allocation: bed reserved in {state['ward']} ward at {state['hospital_name']}"
                )

            state["bed_reserved"] = True
            return state

    state["bed_reserved"] = False
    state["steps"].append(
        f"Bed Allocation: no {state['ward']} beds available at any matching hospital"
    )

    return state