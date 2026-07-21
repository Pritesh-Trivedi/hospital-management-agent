import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
DATA_DIR = BACKEND_DIR / "data"

# Load environment variables from the project root .env first, then backend/.env.
for env_path in [BASE_DIR / ".env", BACKEND_DIR / ".env"]:
    if env_path.exists():
        load_dotenv(env_path, override=False)


def get_env(name, default=None):
    return os.getenv(name, default)
