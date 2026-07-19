import { useState } from 'react'

function PatientForm({ onSubmit, loading }) {
  const [patientName, setPatientName] = useState('')
  const [email, setEmail] = useState('')
  const [age, setAge] = useState('')
  const [symptoms, setSymptoms] = useState('')
  const [errors, setErrors] = useState({})

  const validate = () => {
    const newErrors = {}

    if (!patientName.trim()) {
      newErrors.patientName = 'Patient name is required.'
    }

    if (email.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      newErrors.email = 'Please enter a valid email address.'
    }

    if (!age) {
      newErrors.age = 'Age is required.'
    } else if (Number.isNaN(Number(age)) || Number(age) <= 0 || Number(age) > 120) {
      newErrors.age = 'Enter a valid age between 1 and 120.'
    }

    if (!symptoms.trim()) {
      newErrors.symptoms = 'Please describe the symptoms.'
    } else if (symptoms.trim().length < 5) {
      newErrors.symptoms = 'Please provide a bit more detail about the symptoms.'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!validate()) return

    onSubmit({
      patientName: patientName.trim(),
      email: email.trim(),
      age,
      symptoms: symptoms.trim(),
    })
  }

  return (
    <form className="patient-form" onSubmit={handleSubmit} noValidate>
      <h2 className="form-title">Patient Intake</h2>
      <p className="form-description">
        Enter patient details below. Our AI agent will classify the case and assign an available doctor.
      </p>

      <div className="form-field">
        <label htmlFor="patientName">Patient Name</label>
        <input
          id="patientName"
          type="text"
          placeholder="e.g. Rahul Sharma"
          value={patientName}
          onChange={(e) => setPatientName(e.target.value)}
          disabled={loading}
          className={errors.patientName ? 'input-error' : ''}
        />
        {errors.patientName && <span className="field-error">{errors.patientName}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="email">Email Address (for notification)</label>
        <input
          id="email"
          type="email"
          placeholder="e.g. patient@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={loading}
          className={errors.email ? 'input-error' : ''}
        />
        {errors.email && <span className="field-error">{errors.email}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="age">Age</label>
        <input
          id="age"
          type="number"
          placeholder="e.g. 52"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          disabled={loading}
          className={errors.age ? 'input-error' : ''}
          min="1"
          max="120"
        />
        {errors.age && <span className="field-error">{errors.age}</span>}
      </div>

      <div className="form-field">
        <label htmlFor="symptoms">Symptoms</label>
        <textarea
          id="symptoms"
          placeholder="Describe the symptoms in detail, e.g. Chest pain and difficulty breathing"
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          disabled={loading}
          className={errors.symptoms ? 'input-error' : ''}
          rows={4}
        />
        {errors.symptoms && <span className="field-error">{errors.symptoms}</span>}
      </div>

      <button type="submit" className="submit-btn" disabled={loading}>
        {loading ? 'Processing…' : 'Start Triage'}
      </button>
    </form>
  )
}

export default PatientForm
