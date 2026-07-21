import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from utils.ambulance_utils import create_ambulance_request


def test_create_ambulance_request_returns_expected_shape(tmp_path):
    file_path = tmp_path / 'ambulances.csv'
    request = create_ambulance_request('P1001', 'Emergency', 'Dr. Rao', file_path=file_path)

    assert request['patient_id'] == 'P1001'
    assert request['ward'] == 'Emergency'
    assert request['assigned_doctor'] == 'Dr. Rao'
    assert request['status'] == 'Dispatched'
    assert request['ambulance_id'].startswith('AMB-')
    assert 10 <= request['eta_minutes'] <= 20
    assert file_path.exists()
