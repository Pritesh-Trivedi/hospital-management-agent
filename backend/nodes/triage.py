import json
import os

from langchain_groq import ChatGroq
from config import get_env

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_env("GROQ_API_KEY")
)

triage_prompt = """
You are an expert hospital triage assistant.

Classify the patient into exactly one of these wards:
- Emergency
- General
- Mental Health

Also assign:
- priority: High, Medium, or Low
- guidance: 1-2 sentences of SAFE general advice for while the patient waits for the doctor.
  Do NOT diagnose the patient. Do NOT recommend or name any medication.

Return ONLY valid JSON in this format, with no extra text:

{
    "ward": "...",
    "priority": "...",
    "reason": "...",
    "guidance": "..."
}

Symptoms:
"""

# Hard-coded safety net for ward routing. If any of these appear, the
# patient is force-routed to the correct ward regardless of what the LLM
# said. Ambulance-specific safety logic lives in nodes/ambulance.py.
EMERGENCY_KEYWORDS = [
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

CRISIS_KEYWORDS = [
    "suicide",
    "self-harm",
    "self harm",
    "want to die",
]


def check_ward_safety_keywords(symptoms):
    lower_symptoms = symptoms.lower()
    matched_emergency = [kw for kw in EMERGENCY_KEYWORDS if kw in lower_symptoms]
    matched_crisis = [kw for kw in CRISIS_KEYWORDS if kw in lower_symptoms]
    return matched_emergency, matched_crisis


def triage_node(state):

    prompt = triage_prompt + state["symptoms"]

    response = llm.invoke(prompt)

    result = json.loads(response.content)

    state["ward"] = result["ward"]
    state["priority"] = result["priority"]
    state["reasoning"] = result["reason"]
    state["guidance"] = result.get("guidance", "")

    matched_emergency, matched_crisis = check_ward_safety_keywords(state["symptoms"])

    if matched_emergency:
        state["ward"] = "Emergency"
        state["priority"] = "High"
        state["reasoning"] += " [Safety override applied: critical symptom keywords detected.]"
    elif matched_crisis:
        state["ward"] = "Mental Health"
        state["priority"] = "High"
        state["reasoning"] += " [Safety override applied: crisis-related keywords detected.]"

    print("Ward:", state["ward"])

    state["steps"].append(
        f"Router: classified as {state['ward']} ({state['priority']} priority) — {state['reasoning']}"
    )

    return state