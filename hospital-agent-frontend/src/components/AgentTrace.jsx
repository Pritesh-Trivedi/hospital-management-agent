import { useState } from 'react'

const STEP_ICONS = {
  Intake: '📝',
  Router: '🧭',
  'Ambulance Check': '🚑',
  Location: '📍',
  'Hospital Selection': '🏥',
  'Doctor Availability': '🩺',
  'Admission Decision': '🤔',
  'Bed Allocation': '🛏️',
  Database: '💾',
  'Appointment Booking': '📅',
  'Queue Management': '⏱️',
  Notification: '📣',
  Response: '✅',
}

const WARD_COLOR_VARS = {
  Emergency: '--color-emergency',
  General: '--color-general',
  'Mental Health': '--color-mental',
}

function getStepIcon(step) {
  const label = step.split(':')[0]
  return STEP_ICONS[label] || '●'
}

function getStepLabel(step) {
  const [label, ...rest] = step.split(':')
  return { label, detail: rest.join(':').trim() }
}

function AgentTrace({ steps, ward }) {
  const [expanded, setExpanded] = useState(false)
  const [expandCount, setExpandCount] = useState(0)

  if (!steps || steps.length === 0) return null

  const wardColorVar = WARD_COLOR_VARS[ward]

  const handleToggle = () => {
    if (!expanded) {
      setExpandCount((c) => c + 1) // remounts the list so the stagger-in animation replays
    }
    setExpanded(!expanded)
  }

  return (
    <div className={`thinking-bubble ${expanded ? 'thinking-bubble--expanded' : ''}`}>
      <button
        type="button"
        className="thinking-bubble-toggle"
        onClick={handleToggle}
        aria-expanded={expanded}
      >
        <span className="thinking-bubble-toggle-left">
          <span className="thinking-bubble-toggle-icon" aria-hidden="true">🧠</span>
          <span className="thinking-bubble-toggle-text">
            {expanded ? 'Collapse Thinking' : 'View Thinking'}
          </span>
        </span>
        <span className={`thinking-bubble-arrow ${expanded ? 'thinking-bubble-arrow--open' : ''}`} aria-hidden="true">
          ➜
        </span>
      </button>

      <div className="thinking-bubble-panel">
        <div className="thinking-bubble-panel-inner">
          <h2 className="agent-trace-title">Agent Reasoning Trace</h2>
          <p className="agent-trace-subtitle">
            Live steps the AI agent took to reach its decision
          </p>

          <ol className="agent-trace-list" key={expandCount}>
            {steps.map((step, index) => {
              const { label, detail } = getStepLabel(step)
              const isLast = index === steps.length - 1
              const iconStyle =
                isLast && wardColorVar
                  ? {
                      borderColor: `var(${wardColorVar})`,
                      color: `var(${wardColorVar})`,
                      background: '#fff',
                    }
                  : undefined

              return (
                <li
                  key={index}
                  className="agent-trace-item"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <div className="agent-trace-marker">
                    <span className="agent-trace-icon" style={iconStyle}>
                      {getStepIcon(step)}
                    </span>
                    {!isLast && <span className="agent-trace-line" />}
                  </div>
                  <div className="agent-trace-content">
                    <span className="agent-trace-label">{label}</span>
                    <p className="agent-trace-detail">{detail}</p>
                  </div>
                </li>
              )
            })}
          </ol>
        </div>
      </div>
    </div>
  )
}

export default AgentTrace
