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

  const hasCoords = data.hospital_latitude && data.hospital_longitude
  const directionsUrl = hasCoords
    ? `https://www.google.com/maps/dir/?api=1&destination=${data.hospital_latitude},${data.hospital_longitude}`
    : `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(
        data.hospital_address || data.hospital_name || ''
      )}`

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
          <div>
            <strong>Ambulance Recommended — {data.emergency_level} Level</strong>
            <p>{data.ambulance_reasoning}</p>
          </div>
        </div>
      )}

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
          <span className="result-value">{data.assigned_doctor}</span>
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
          <span className="result-value result-value--mono">{data.next_slot}</span>
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
