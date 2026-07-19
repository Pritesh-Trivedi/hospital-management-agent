from langgraph.graph import StateGraph, END
from state import HospitalState

from nodes.intake import intake_node
from nodes.triage import triage_node
from nodes.ambulance import ambulance_node
from nodes.location import location_node
from nodes.hospital_selection import hospital_selection_node
from nodes.doctor import doctor_node
from nodes.admission import admission_node
from nodes.bed_allocation import bed_allocation_node
from nodes.database import database_node
from nodes.appointment import appointment_node
from nodes.queue_management import queue_management_node
from nodes.notification import notification_node
from nodes.response import response_node

builder = StateGraph(HospitalState)

builder.add_node("intake", intake_node)
builder.add_node("triage", triage_node)
builder.add_node("ambulance", ambulance_node)
builder.add_node("location", location_node)
builder.add_node("hospital_selection", hospital_selection_node)
builder.add_node("doctor", doctor_node)
builder.add_node("admission", admission_node)
builder.add_node("bed_allocation", bed_allocation_node)
builder.add_node("database", database_node)
builder.add_node("appointment", appointment_node)
builder.add_node("queue_management", queue_management_node)
builder.add_node("notification", notification_node)
builder.add_node("response", response_node)

builder.set_entry_point("intake")

builder.add_edge("intake", "triage")
builder.add_edge("triage", "ambulance")                  # Added
builder.add_edge("ambulance", "location")                 # Changed
builder.add_edge("location", "hospital_selection")
builder.add_edge("hospital_selection", "doctor")
builder.add_edge("doctor", "admission")                   # Added
builder.add_edge("admission", "bed_allocation")            # Changed
builder.add_edge("bed_allocation", "database")
builder.add_edge("database", "appointment")
builder.add_edge("appointment", "queue_management")
builder.add_edge("queue_management", "notification")
builder.add_edge("notification", "response")
builder.add_edge("response", END)

graph = builder.compile()