import pandas as pd
from datetime import datetime
from config import DATA_DIR

def generate_patient_id():

    patients = pd.read_csv(DATA_DIR / "patients.csv")

    if len(patients) == 0:
        return "P1001"

    last_id = patients.iloc[-1]["patient_id"]

    number = int(last_id[1:])

    return f"P{number + 1}"
def save_patient(state):

    patients = pd.read_csv(DATA_DIR / "patients.csv")

    patient_id = generate_patient_id()

    new_patient = {
        "patient_id": patient_id,
        "name": state["patient_name"],
        "age": state["age"],
        "symptoms": state["symptoms"],
        "ward": state["ward"],
        "priority": state["priority"],
        "doctor": state["assigned_doctor"],
        "admission_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    patients = pd.concat(
        [patients, pd.DataFrame([new_patient])],
        ignore_index=True
    )

    patients.to_csv(DATA_DIR / "patients.csv", index=False)

    return patient_id