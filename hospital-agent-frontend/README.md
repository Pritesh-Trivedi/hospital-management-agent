# Hospital Management Agent — Frontend

React (Vite) frontend for the Hospital Management Agentic AI project.
Talks to your existing FastAPI backend at `http://localhost:8000/triage`.

## Folder structure

```
hospital-agent-frontend/
├── index.html
├── package.json
├── vite.config.js
├── .gitignore
├── README.md
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    ├── index.css
    └── components/
        ├── PatientForm.jsx
        └── ResultCard.jsx
```

## 1. Install Node.js

You need Node.js 18+ installed. Check with:

```bash
node -v
npm -v
```

## 2. Install dependencies

From inside the `hospital-agent-frontend` folder:

```bash
npm install
```

This installs React, Vite, and axios (axios is already listed in
`package.json`, so a single `npm install` pulls it in — no separate command
needed).

## 3. Start your backend first

In a separate terminal, start your FastAPI backend so it's listening on
`http://localhost:8000`:

```bash
uvicorn main:app --reload --port 8000
```

(Use whatever command you already use to run your FastAPI app — just make
sure it ends up on port 8000, since that's what the frontend calls.)

## 4. Start the frontend

```bash
npm run dev
```

Vite will print a local URL, typically:

```
http://localhost:5173
```

Open that in your browser.

## 5. Using the app

1. Enter Patient Name, Age, and Symptoms.
2. Click **Start Triage**.
3. The app calls `POST http://localhost:8000/triage` with your form data.
4. While waiting, a loading spinner is shown and the button is disabled.
5. On success, a result card appears showing ward, priority, assigned
   doctor, status, next slot, patient ID, notification ID, and the AI's
   reasoning.
6. If the backend is unreachable or returns an error, a clear error message
   is shown instead of a blank screen.

## Notes

- The ward badge changes color automatically: **Emergency = red**,
  **General = blue**, **Mental Health = purple**.
- The priority badge changes color automatically: **High = red**,
  **Medium = orange**, **Low = green**.
- If your backend runs on a different host/port, change `API_URL` at the
  top of `src/App.jsx`.
- CORS: if the browser blocks the request with a CORS error, add
  `CORSMiddleware` to your FastAPI app allowing `http://localhost:5173`.

## Build for production

```bash
npm run build
npm run preview
```

`npm run build` outputs static files to `dist/`, which you can deploy
anywhere (e.g. Vercel) — just make sure `API_URL` in `App.jsx` points to
your deployed backend URL instead of `localhost`.
