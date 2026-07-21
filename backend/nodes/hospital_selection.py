import pandas as pd
from langchain_groq import ChatGroq

from config import DATA_DIR, get_env
from utils.location_utils import haversine_distance_km

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_env("GROQ_API_KEY")
)

# Weights for the scoring formula — tweak these if you want distance
# or rating to matter more/less in the decision.
WEIGHT_DISTANCE = 0.5
WEIGHT_RATING = 0.3
WEIGHT_QUEUE = 0.2


def score_hospital(distance_km, rating, queue_length):
    distance_score = 1 / (distance_km + 1)
    rating_score = rating / 5
    queue_score = 1 / (queue_length + 1)

    return (
        WEIGHT_DISTANCE * distance_score
        + WEIGHT_RATING * rating_score
        + WEIGHT_QUEUE * queue_score
    )


def hospital_selection_node(state):

    ward = state["ward"].strip().lower().replace(" ", "_")

    hospitals = pd.read_csv(DATA_DIR / "hospitals.csv")

    # Keep only hospitals that support this ward
    matching = hospitals[
        hospitals["specialties"].str.lower().str.contains(ward)
    ].copy()

    if matching.empty:
        # No hospital supports this ward — fall back to considering all
        # hospitals rather than failing the whole pipeline.
        matching = hospitals.copy()

    matching["distance_km"] = matching.apply(
        lambda row: haversine_distance_km(
            state["patient_latitude"],
            state["patient_longitude"],
            row["latitude"],
            row["longitude"],
        ),
        axis=1,
    )

    matching["score"] = matching.apply(
        lambda row: score_hospital(row["distance_km"], row["rating"], row["queue_length"]),
        axis=1,
    )

    best = matching.sort_values("score", ascending=False).iloc[0]

    state["hospital_id"] = best["hospital_id"]
    state["hospital_name"] = best["hospital_name"]
    state["hospital_address"] = best["address"]
    state["hospital_latitude"] = float(best["latitude"])
    state["hospital_longitude"] = float(best["longitude"])
    state["hospital_distance_km"] = float(best["distance_km"])

    reasoning_prompt = f"""
You are a hospital operations AI. In 1-2 sentences, explain why this hospital
was selected for the patient. Be specific and reference the actual numbers.
Do not use markdown or lists.

Hospital: {best['hospital_name']}
Distance: {best['distance_km']} km
Rating: {best['rating']} / 5
Current queue length: {best['queue_length']}
Ward needed: {state['ward']}
Patient priority: {state['priority']}
"""

    try:
        response = llm.invoke(reasoning_prompt)
        hospital_reasoning = response.content.strip()
    except Exception:
        hospital_reasoning = (
            f"{best['hospital_name']} selected: {best['distance_km']} km away, "
            f"rated {best['rating']}/5, with a current queue of {best['queue_length']} patients."
        )

    state["hospital_reasoning"] = hospital_reasoning

    print("Selected Hospital:", state["hospital_name"], "-", state["hospital_distance_km"], "km")

    state["steps"].append(
        f"Hospital Selection: chose {best['hospital_name']} ({best['distance_km']} km away) — {hospital_reasoning}"
    )

    return state