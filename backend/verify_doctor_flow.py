import shutil
from pathlib import Path
import pandas as pd
import sys

sys.path.append(str(Path(__file__).resolve().parent))
from utils.doctor_utils import get_available_doctors, change_doctor

root = Path(__file__).resolve().parent
patients_path = root / 'data' / 'patients.csv'
doctors_path = root / 'data' / 'doctors.csv'
backup_dir = root / '__tmp_backup__'
backup_dir.mkdir(exist_ok=True)
shutil.copy2(patients_path, backup_dir / 'patients.csv')
shutil.copy2(doctors_path, backup_dir / 'doctors.csv')

try:
    patients = pd.read_csv(patients_path)
    before = patients.loc[patients['patient_id'] == 'P1001', 'doctor'].iloc[0]
    available = get_available_doctors('Emergency', 'Dr. Rao')
    result = change_doctor('P1001', 'Dr. Khan')
    after = pd.read_csv(patients_path).loc[pd.read_csv(patients_path)['patient_id'] == 'P1001', 'doctor'].iloc[0]
    print({'before': before, 'available_count': len(available), 'result': result, 'after': after})
finally:
    shutil.copy2(backup_dir / 'patients.csv', patients_path)
    shutil.copy2(backup_dir / 'doctors.csv', doctors_path)
    shutil.rmtree(backup_dir)
