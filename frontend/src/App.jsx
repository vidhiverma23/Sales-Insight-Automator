import React, { useState } from 'react'
import Header from './components/Header'
import FileUploader from './components/FileUploader'
import StatusFeedback from './components/StatusFeedback'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getActiveStep(status) {
  if (!status) return 1
  if (status === 'loading') return 2
  if (status === 'success') return 3
  return 1
}

export default function App() {
  const [file, setFile] = useState(null)
  const [email, setEmail] = useState('')
  const [status, setStatus] = useState(null)      // null | 'loading' | 'success' | 'error'
  const [message, setMessage] = useState('')

  const activeStep = getActiveStep(status)

  const canSubmit = file && email.trim() && !status

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!canSubmit) return

    setStatus('loading')
    setMessage('Parsing your data and generating the AI summary... This may take a moment.')

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('email', email.trim())

      const response = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || `Request failed (${response.status})`)
      }

      setStatus('success')
      setMessage(`Your sales insight report has been sent to ${email}. Check your inbox!`)
    } catch (err) {
      setStatus('error')
      setMessage(err.message || 'An unexpected error occurred. Please try again.')
    }
  }

  const handleReset = () => {
    setFile(null)
    setEmail('')
    setStatus(null)
    setMessage('')
  }

  return (
    <div className="app">
      <Header />

      {/* Steps Indicator */}
      <div className="steps">
        {[
          { num: 1, label: 'Upload' },
          { num: 2, label: 'Analyze' },
          { num: 3, label: 'Deliver' },
        ].map((s) => (
          <div
            key={s.num}
            className={`step ${activeStep === s.num ? 'step--active' : ''} ${
              activeStep > s.num ? 'step--done' : ''
            }`}
          >
            <div className="step__number">
              {activeStep > s.num ? '✓' : s.num}
            </div>
            <span className="step__label">{s.label}</span>
          </div>
        ))}
      </div>

      {/* Main Card */}
      <form className="card" onSubmit={handleSubmit}>
        <FileUploader
          file={file}
          onFileSelect={setFile}
          onRemove={() => setFile(null)}
          disabled={status === 'loading'}
        />

        <div className="form-group">
          <label className="form-group__label" htmlFor="email-input">
            Recipient Email
          </label>
          <input
            id="email-input"
            type="email"
            className="form-group__input"
            placeholder="executive@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={status === 'loading'}
            required
          />
        </div>

        {status === 'success' || status === 'error' ? (
          <button
            type="button"
            className="submit-btn"
            onClick={handleReset}
          >
            {status === 'success' ? '🚀 Generate Another Report' : '🔄 Try Again'}
          </button>
        ) : (
          <button
            type="submit"
            className={`submit-btn ${status === 'loading' ? 'submit-btn--loading' : ''}`}
            disabled={!canSubmit}
          >
            {status === 'loading' ? 'Generating Report...' : '🚀 Generate & Send Report'}
          </button>
        )}

        <StatusFeedback status={status} message={message} />
      </form>

      {/* Footer */}
      <footer className="footer">
        <p className="footer__text">
          Powered by{' '}
          <a
            href="https://rabbittai.com"
            className="footer__link"
            target="_blank"
            rel="noopener noreferrer"
          >
            Rabbitt AI
          </a>{' '}
          · Built with Gemini AI
        </p>
      </footer>
    </div>
  )
}
