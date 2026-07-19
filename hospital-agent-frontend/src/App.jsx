import { useEffect, useRef, useState } from 'react'
import axios from 'axios'
import PatientForm from './components/PatientForm.jsx'
import ResultCard from './components/ResultCard.jsx'
import AgentTrace from './components/AgentTrace.jsx'
import LocationGate from './components/LocationGate.jsx'
import './App.css'

const API_URL = 'https://hospital-management-agent.onrender.com/triage'

function App() {
  const [location, setLocation] = useState(null) // { latitude, longitude }
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const resultRef = useRef(null)

  useEffect(() => {
    if (result && resultRef.current) {
      // Small delay so the pop-in animation has already started before we scroll,
      // which reads much better than an instant jump.
      const timer = setTimeout(() => {
        resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 150)
      return () => clearTimeout(timer)
    }
  }, [result])

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post(API_URL, {
        patient_name: formData.patientName,
        email: formData.email,
        age: Number(formData.age),
        symptoms: formData.symptoms,
        latitude: location?.latitude,
        longitude: location?.longitude,
      })
      setResult(response.data)
    } catch (err) {
      if (err.response) {
        setError(
          `Server error (${err.response.status}): ${err.response.data?.detail || 'Unable to process triage request.'
          }`
        )
      } else if (err.request) {
        setError(
          'Could not reach the backend server. Make sure it is running at http://localhost:8000.'
        )
      } else {
        setError('Something went wrong while submitting the form. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  if (!location) {
    return <LocationGate onConfirm={setLocation} />
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header-top">
          <div className="app-header-brand">
            <div className="app-header-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M12 21C12 21 4 15.5 4 9.5C4 6.46 6.46 4 9.5 4C10.99 4 12.37 4.68 13.29 5.79L12 7.5L13.29 5.79C14.21 4.68 15.59 4 17.08 4C20.12 4 22.58 6.46 22.58 9.5C22.58 15.5 14.58 21 14.58 21"
                  stroke="currentColor"
                  strokeWidth="1.6"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </div>
            <div>
              <span className="app-eyebrow">Autonomous Triage System</span>
              <h1>Hospital Management Agent</h1>
              <p className="app-subtitle">AI-powered patient intake &amp; ward routing</p>
            </div>
          </div>

          <div className="agent-status-pill">
            <span className="agent-status-dot" aria-hidden="true"></span>
            Agent Online
          </div>
        </div>

        <svg
          className="pulse-line"
          viewBox="0 0 800 60"
          preserveAspectRatio="none"
          aria-hidden="true"
        >
          <path
            className="pulse-line-path"
            d="M0,30 L180,30 L205,30 L220,8 L235,52 L250,30 L270,30 L290,15 L305,45 L320,30 L800,30"
            fill="none"
          />
        </svg>
      </header>

      <main className="app-main">
        <div className="location-confirmed-banner">
          📍 Location set
          <button
            type="button"
            className="location-change-link"
            onClick={() => setLocation(null)}
          >
            Change
          </button>
        </div>

        <PatientForm onSubmit={handleSubmit} loading={loading} />

        {loading && (
          <div className="status-panel" role="status" aria-live="polite">
            <span className="spinner" aria-hidden="true"></span>
            <span>Analyzing symptoms and assigning a doctor…</span>
          </div>
        )}

        {error && (
          <div className="status-panel status-panel--error" role="alert">
            <span className="status-panel-icon" aria-hidden="true">⚠</span>
            <span>{error}</span>
          </div>
        )}

        {result && !loading && (
          <div className="result-reveal" ref={resultRef}>
            <AgentTrace steps={result.steps} ward={result.ward} />
            <ResultCard data={result} />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>IBM SkillsBuild Internship Project · Hospital Management Agentic AI</p>
      </footer>
    </div>
  )
}

export default App
