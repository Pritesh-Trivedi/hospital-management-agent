import json

from langchain_groq import ChatGroq
from config import get_env

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=get_env("GROQ_API_KEY")
)

admission_prompt = """
You are a hospital admissions assistant. Based on the patient's ward,
priority, age, and symptoms, decide whether they need to be admitted
(occupy a bed) or can be treated as an outpatient and sent home after
consultation.

Return ONLY valid JSON in this format, with no extra text:

{
    "admission_required": true or false,
    "admission_reasoning": "..."
}
"""


def admission_node(state):

    prompt = (
        admission_prompt
        + f"\nWard: {state['ward']}"
        + f"\nPriority: {state['priority']}"
        + f"\nAge: {state['age']}"
        + f"\nSymptoms: {state['symptoms']}"
    )

    try:
        response = llm.invoke(prompt)
        result = json.loads(response.content)

        state["admission_required"] = bool(result.get("admission_required", False))
        state["admission_reasoning"] = result.get("admission_reasoning", "")
    except Exception:
        # Fail safe: if the LLM call breaks, fall back to a simple rule
        # rather than crashing the whole pipeline right before a demo.
        state["admission_required"] = state["priority"] == "High"
        state["admission_reasoning"] = (
            "Admission assessment unavailable; defaulted based on priority level."
        )

    print("Admission Required:", state["admission_required"])

    state["steps"].append(
        f"Admission Decision: {'admission required' if state['admission_required'] else 'outpatient, no admission needed'} — {state['admission_reasoning']}"
    )

    return state