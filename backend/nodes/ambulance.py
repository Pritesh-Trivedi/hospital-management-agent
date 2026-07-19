import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

ambulance_prompt = """
You are an emergency medical dispatch assistant. Assess whether this patient
needs an ambulance, independent of which hospital ward they were routed to.

Return ONLY valid JSON in this format, with no extra text:

{
    "emergency_level": "Critical" or "Moderate" or "Low",
    "ambulance_recommended": true or false,
    "ambulance_reasoning": "..."
}

Examples of situations that warrant an ambulance: heart attack, stroke,
major accident, unconscious patient, severe breathing difficulty, heavy
bleeding.

Symptoms:
"""

# This node has its own independent safety net, separate from the Router's.
# Even if this LLM call fails to flag a case, these keywords force an
# ambulance recommendation regardless of the model's output.
CRITICAL_KEYWORDS = [
    "chest pain",
    "can't breathe",
    "cant breathe",
    "cannot breathe",
    "not breathing",
    "difficulty breathing",
    "unconscious",
    "heart attack",
    "stroke",
    "severe bleeding",
    "heavy bleeding",
    "major accident",
]


def check_critical_keywords(symptoms):
    lower_symptoms = symptoms.lower()
    return [kw for kw in CRITICAL_KEYWORDS if kw in lower_symptoms]


def ambulance_node(state):

    prompt = ambulance_prompt + state["symptoms"]

    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)

        state["emergency_level"] = result.get("emergency_level", "Low")
        state["ambulance_recommended"] = bool(result.get("ambulance_recommended", False))
        state["ambulance_reasoning"] = result.get("ambulance_reasoning", "")
    except Exception:
        # If the LLM call fails or returns malformed JSON, fail safe rather
        # than silently skipping the ambulance check.
        state["emergency_level"] = "Low"
        state["ambulance_recommended"] = False
        state["ambulance_reasoning"] = "Ambulance assessment unavailable; defaulted to no recommendation."

    matched = check_critical_keywords(state["symptoms"])

    if matched:
        state["emergency_level"] = "Critical"
        state["ambulance_recommended"] = True
        state["ambulance_reasoning"] = (
            f"Safety override: symptom description matched critical keyword(s) "
            f"({', '.join(matched)}). Ambulance recommended regardless of AI assessment."
        )

    print("Ambulance Recommended:", state["ambulance_recommended"], "-", state["emergency_level"])

    if state["ambulance_recommended"]:
        state["steps"].append(
            f"Ambulance Check: ambulance recommended ({state['emergency_level']} level) — {state['ambulance_reasoning']}"
        )
    else:
        state["steps"].append(
            f"Ambulance Check: no ambulance needed ({state['emergency_level']} level) — {state['ambulance_reasoning']}"
        )

    return state