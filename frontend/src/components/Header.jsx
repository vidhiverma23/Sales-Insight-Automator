import React from 'react'

export default function Header() {
  return (
    <header className="header">
      <div className="header__logo">
        <span className="header__icon">🐇</span>
        <span className="header__brand">Rabbitt AI</span>
      </div>
      <h1 className="header__title">Sales Insight Automator</h1>
      <p className="header__subtitle">
        Upload your sales data and receive an AI-generated executive brief
        delivered straight to your inbox.
      </p>
    </header>
  )
}
