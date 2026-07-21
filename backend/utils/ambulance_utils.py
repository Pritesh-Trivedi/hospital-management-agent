import csv
import random
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'
AMBULANCE_FILE = DATA_DIR / 'ambulances.csv'


def _ensure_file_exists(file_path=None):
    path = Path(file_path or AMBULANCE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open('w', newline='', encoding='utf-8') as handle:
            writer = csv.writer(handle)
            writer.writerow(['ambulance_id', 'patient_id', 'ward', 'assigned_doctor', 'eta_minutes', 'status', 'created_at'])
    return path


def create_ambulance_request(patient_id, ward=None, assigned_doctor=None, file_path=None):
    path = _ensure_file_exists(file_path)

    eta_minutes = random.randint(10, 20)
    ambulance_id = f"AMB-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(100, 999)}"

    record = {
        'ambulance_id': ambulance_id,
        'patient_id': patient_id,
        'ward': ward or '',
        'assigned_doctor': assigned_doctor or '',
        'eta_minutes': eta_minutes,
        'status': 'Dispatched',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    with path.open('a', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(record.keys()))
        if path.stat().st_size == 0:
            writer.writeheader()
        writer.writerow(record)

    return record
