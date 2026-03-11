import React from 'react'

export default function StatusFeedback({ status, message }) {
  if (!status) return null

  const config = {
    loading: {
      icon: null,
      title: 'Processing your data...',
      className: 'status--loading',
      showSpinner: true,
    },
    success: {
      icon: '✅',
      title: 'Report Sent Successfully!',
      className: 'status--success',
      showSpinner: false,
    },
    error: {
      icon: '❌',
      title: 'Something went wrong',
      className: 'status--error',
      showSpinner: false,
    },
  }

  const c = config[status]
  if (!c) return null

  return (
    <div className={`status ${c.className}`}>
      {c.showSpinner ? (
        <div className="spinner" />
      ) : (
        <span className="status__icon">{c.icon}</span>
      )}
      <div className="status__content">
        <div className="status__title">{c.title}</div>
        {message && <div className="status__message">{message}</div>}
      </div>
    </div>
  )
}
