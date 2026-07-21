# Hospital Management Agent

## Quick start for a fresh clone

1. Copy the example environment file:
   - Windows PowerShell: `Copy-Item .env.example .env`
   - Linux/macOS: `cp .env.example .env`
2. Edit `.env` and fill in your own Groq and EmailJS credentials.
3. Create and activate a Python virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1` (Windows PowerShell)
4. Install Python dependencies:
   - `pip install -r backend/requirements.txt`
5. Start the backend:
   - `uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000`
6. Start the frontend:
   - `cd hospital-agent-frontend`
   - `npm install`
   - `npm run dev`

## Email setup (optional but recommended)

The application can send appointment and triage emails through EmailJS. To enable this feature:

1. Create an account at https://www.emailjs.com/
2. Create an Email Service and note the Service ID.
3. Create an Email Template and note the Template ID.
4. Copy your Public Key and Private Key from the EmailJS dashboard.
5. Add the following values to your `.env` file:
   - `EMAILJS_SERVICE_ID`
   - `EMAILJS_TEMPLATE_ID`
   - `EMAILJS_PUBLIC_KEY`
   - `EMAILJS_PRIVATE_KEY`

If these values are not provided, the app will continue in development mode and will not break the workflow.

## Notes
- The backend loads environment variables from the repository root `.env` first, then `backend/.env`.
- The application uses a CSV-based data store under `backend/data`.
- If EmailJS credentials are not configured, the app will continue in development mode without exposing raw provider errors.
