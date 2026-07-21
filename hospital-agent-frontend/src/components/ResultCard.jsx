import { useEffect, useState } from 'react'
import axios from 'axios'

const WARD_STYLES = {
  Emergency: { className: 'ward-emergency', label: 'Emergency' },
  General: { className: 'ward-general', label: 'General' },
  'Mental Health': { className: 'ward-mental', label: 'Mental Health' },
}

const PRIORITY_STYLES = {
  High: 'priority-high',
  Medium: 'priority-medium',
  Low: 'priority-low',
}

function getWardStyle(ward) {
  return WARD_STYLES[ward] || { className: 'ward-general', label: ward }
}

function getPriorityStyle(priority) {
  return PRIORITY_STYLES[priority] || 'priority-medium'
}

function ResultCard({ data }) {
  const wardStyle = getWardStyle(data.ward)
  const priorityStyle = getPriorityStyle(data.priority)
  const [showDoctorPicker, setShowDoctorPicker] = useState(false)
  const [availableDoctors, setAvailableDoctors] = useState([])
  const [selectedDoctor, setSelectedDoctor] = useState(data.assigned_doctor || '')
  const [doctorLoading, setDoctorLoading] = useState(false)
  const [doctorError, setDoctorError] = useState('')
  const [doctorSuccess, setDoctorSuccess] = useState('')
  const [ambulanceLoading, setAmbulanceLoading] = useState(false)
  const [ambulanceError, setAmbulanceError] = useState('')
  const [ambulanceDetails, setAmbulanceDetails] = useState(null)
  const [displayDoctor, setDisplayDoctor] = useState(data.assigned_doctor || '')
  const [displayNextSlot, setDisplayNextSlot] = useState(data.next_slot || '')
  const [displaySlotMinutes, setDisplaySlotMinutes] = useState(data.slot_minutes || '')

  const hasCoords = data.hospital_latitude && data.hospital_longitude
  const directionsUrl = hasCoords
    ? `https://www.google.com/maps/dir/?api=1&destination=${data.hospital_latitude},${data.hospital_longitude}`
    : `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(
        data.hospital_address || data.hospital_name || ''
      )}`

  const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? '/api' : 'https://hospital-management-agent.onrender.com')

  useEffect(() => {
    setSelectedDoctor(data.assigned_doctor || '')
    setDisplayDoctor(data.assigned_doctor || '')
    setDisplayNextSlot(data.next_slot || '')
    setDisplaySlotMinutes(data.slot_minutes || '')
    setShowDoctorPicker(false)
    setAvailableDoctors([])
    setDoctorError('')
    setDoctorSuccess('')
    setAmbulanceError('')
    setAmbulanceDetails(null)
  }, [data.assigned_doctor, data.next_slot, data.slot_minutes, data.patient_id])

  const fetchDoctors = async () => {
    if (!data.ward) return

    setDoctorLoading(true)
    setDoctorError('')
    setDoctorSuccess('')

    try {
      const response = await axios.get(`${API_BASE_URL}/doctors?ward=${encodeURIComponent(data.ward)}`)
      const doctors = response.data?.available_doctors || []
      setAvailableDoctors(doctors)
      if (doctors.length > 0) {
        setSelectedDoctor(doctors[0].doctor_name)
        setShowDoctorPicker(true)
      } else {
        setDoctorError('No alternative doctors are available for this ward right now.')
      }
    } catch (err) {
      setDoctorError('Unable to load doctor options right now.')
    } finally {
      setDoctorLoading(false)
    }
  }

  const handleDoctorChange = async () => {
    if (!data.patient_id || !selectedDoctor) return

    setDoctorLoading(true)
    setDoctorError('')
    setDoctorSuccess('')

    try {
      const response = await axios.post(`${API_BASE_URL}/change-doctor`, {
        patient_id: data.patient_id,
        doctor_name: selectedDoctor,
      })

      if (response.data?.doctor) {
        setDisplayDoctor(response.data.doctor)
        setDisplayNextSlot(response.data.next_slot)
        setDisplaySlotMinutes(response.data.slot_minutes)
        setSelectedDoctor(response.data.doctor)
        setShowDoctorPicker(false)
        setDoctorSuccess('Doctor updated successfully.')
      } else {
        setDoctorError('The doctor update did not return a new assignment.')
      }
    } catch (err) {
      setDoctorError('Unable to update the doctor assignment right now.')
    } finally {
      setDoctorLoading(false)
    }
  }

  const handleCallAmbulance = async () => {
    if (!data.patient_id) return

    setAmbulanceLoading(true)
    setAmbulanceError('')

    try {
      const response = await axios.post(`${API_BASE_URL}/call-ambulance`, {
        patient_id: data.patient_id,
        ward: data.ward,
        assigned_doctor: data.assigned_doctor,
      })

      setAmbulanceDetails(response.data)
    } catch (err) {
      setAmbulanceError('Unable to dispatch the ambulance right now.')
    } finally {
      setAmbulanceLoading(false)
    }
  }

  return (
    <div className={`result-card ${wardStyle.className}`}>
      <div className="result-card-header">
        <h2>Triage Result</h2>
        <div className="badge-group">
          <span className={`badge ${wardStyle.className}`}>{wardStyle.label}</span>
          <span className={`badge ${priorityStyle}`}>{data.priority} Priority</span>
        </div>
      </div>

      {data.ambulance_recommended && (
        <div className="ambulance-banner">
          <span className="ambulance-banner-icon" aria-hidden="true">🚑</span>
          <div className="ambulance-banner-content">
            <strong>Ambulance Recommended — {data.emergency_level} Level</strong>
            <p>{data.ambulance_reasoning}</p>
            <div className="ambulance-banner-actions">
              <button type="button" className="submit-btn" onClick={handleCallAmbulance} disabled={ambulanceLoading}>
                {ambulanceLoading ? 'Dispatching…' : 'Call Ambulance'}
              </button>
            </div>
          </div>
        </div>
      )}

      {ambulanceDetails && (
        <div className="ambulance-request-card" role="status">
          <div className="ambulance-request-title">Ambulance Request</div>
          <div className="ambulance-request-grid">
            <div className="result-item">
              <span className="result-label">Ambulance ID</span>
              <span className="result-value">{ambulanceDetails.ambulance_id}</span>
            </div>
            <div className="result-item">
              <span className="result-label">ETA</span>
              <span className="result-value">{ambulanceDetails.eta_minutes} min</span>
            </div>
            <div className="result-item">
              <span className="result-label">Status</span>
              <span className="result-value">{ambulanceDetails.status}</span>
            </div>
          </div>
        </div>
      )}

      {ambulanceError && <p className="doctor-feedback doctor-feedback--error">{ambulanceError}</p>}

      {/* Hospital */}
      <div className="result-section-heading">Selected Hospital</div>
      <div className="hospital-info-block">
        <div className="hospital-info-main">
          <span className="hospital-name">{data.hospital_name}</span>
          <span className="hospital-address">{data.hospital_address}</span>
        </div>
        <span className="hospital-distance-badge">{data.hospital_distance_km} km away</span>
      </div>

      <a href={directionsUrl} target="_blank" rel="noopener noreferrer" className="directions-btn">
        📍 Get Directions
      </a>

      <div className="reasoning-box">
        <span className="result-label">Why This Hospital</span>
        <p>{data.hospital_reasoning}</p>
      </div>

      {/* Patient */}
      <div className="result-section-heading">Patient</div>
      <div className="result-grid">
        <div className="result-item">
          <span className="result-label">Patient Name</span>
          <span className="result-value">{data.patient_name}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Age</span>
          <span className="result-value">{data.age}</span>
        </div>
        {data.email && (
          <div className="result-item">
            <span className="result-label">Email Address</span>
            <span className="result-value">{data.email}</span>
          </div>
        )}
        {data.email_status && (
          <div className="result-item">
            <span className="result-label">Email Notification</span>
            <span className="result-value">{data.email_status}</span>
          </div>
        )}
        <div className="result-item result-item--wide">
          <span className="result-label">Symptoms</span>
          <span className="result-value">{data.symptoms}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Assigned Doctor</span>
          <span className="result-value">{displayDoctor || data.assigned_doctor}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Status</span>
          <span className="result-value">{data.status}</span>
        </div>
      </div>

      {/* Admission + Bed */}
      <div className="result-section-heading">Admission &amp; Bed</div>
      <div className="result-grid">
        <div className="result-item">
          <span className="result-label">Admission Required</span>
          <span className="result-value">{data.admission_required ? 'Yes' : 'No'}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Bed Reserved</span>
          <span className="result-value">
            {data.admission_required ? (data.bed_reserved ? 'Yes' : 'No beds available') : 'Not required'}
          </span>
        </div>
        <div className="result-item result-item--wide">
          <span className="result-label">Admission Reasoning</span>
          <span className="result-value">{data.admission_reasoning}</span>
        </div>
      </div>

      {/* Appointment + Queue */}
      <div className="result-section-heading">Appointment &amp; Queue</div>
      <div className="result-grid">
        <div className="result-item">
          <span className="result-label">Appointment Time</span>
          <span className="result-value result-value--mono">{displayNextSlot || data.next_slot}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Token Number</span>
          <span className="result-value result-value--mono">{data.token_number}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Consultation Room</span>
          <span className="result-value result-value--mono">{data.consultation_room}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Appointment ID</span>
          <span className="result-value result-value--mono">{data.appointment_id}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Queue Position</span>
          <span className="result-value result-value--mono">#{data.queue_position}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Estimated Wait</span>
          <span className="result-value result-value--mono">{data.estimated_wait_minutes} min</span>
        </div>
        <div className="result-item">
          <span className="result-label">Patient ID</span>
          <span className="result-value result-value--mono">{data.patient_id}</span>
        </div>
        <div className="result-item">
          <span className="result-label">Notification ID</span>
          <span className="result-value result-value--mono">{data.notification_id}</span>
        </div>
      </div>

      <div className="doctor-change-panel">
        <div className="doctor-change-header">
          <span className="result-label">Doctor Preference</span>
          <button type="button" className="doctor-change-btn" onClick={fetchDoctors} disabled={doctorLoading}>
            {doctorLoading ? 'Loading…' : 'Change Doctor'}
          </button>
        </div>

        {showDoctorPicker && (
          <div className="doctor-change-controls">
            <label className="doctor-select-label" htmlFor="doctor-select">
              Available doctors for {data.ward}
            </label>
            <select
              id="doctor-select"
              className="doctor-select"
              value={selectedDoctor}
              onChange={(event) => setSelectedDoctor(event.target.value)}
            >
              {availableDoctors.map((doctor) => (
                <option key={doctor.doctor_name} value={doctor.doctor_name}>
                  {doctor.doctor_name} · {doctor.next_slot}
                </option>
              ))}
            </select>
            <button type="button" className="submit-btn doctor-confirm-btn" onClick={handleDoctorChange} disabled={doctorLoading}>
              {doctorLoading ? 'Updating…' : 'Confirm Change'}
            </button>
          </div>
        )}

        {doctorError && <p className="doctor-feedback doctor-feedback--error">{doctorError}</p>}
        {doctorSuccess && <p className="doctor-feedback doctor-feedback--success">{doctorSuccess}</p>}
      </div>

      {/* Guidance + Reasoning */}
      {data.guidance && (
        <div className="reasoning-box reasoning-box--guidance">
          <span className="result-label">While You Wait</span>
          <p>{data.guidance}</p>
        </div>
      )}

      <div className="reasoning-box">
        <span className="result-label">AI Reasoning</span>
        <p>{data.reasoning}</p>
      </div>
    </div>
  )
}

export default ResultCard
