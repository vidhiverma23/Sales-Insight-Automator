import React, { useState, useRef, useCallback } from 'react'

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const ALLOWED_TYPES = [
  'text/csv',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-excel',
]
const ALLOWED_EXTENSIONS = ['.csv', '.xlsx', '.xls']

export default function FileUploader({ file, onFileSelect, onRemove, disabled }) {
  const [isDragActive, setIsDragActive] = useState(false)
  const inputRef = useRef(null)

  const validateFile = (f) => {
    const ext = '.' + f.name.split('.').pop().toLowerCase()
    if (!ALLOWED_EXTENSIONS.includes(ext) && !ALLOWED_TYPES.includes(f.type)) {
      alert('Please upload a .csv or .xlsx file.')
      return false
    }
    if (f.size > 10 * 1024 * 1024) {
      alert('File is too large. Maximum size is 10 MB.')
      return false
    }
    return true
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setIsDragActive(false)
    if (disabled) return
    const dropped = e.dataTransfer.files[0]
    if (dropped && validateFile(dropped)) {
      onFileSelect(dropped)
    }
  }, [disabled, onFileSelect])

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    if (!disabled) setIsDragActive(true)
  }, [disabled])

  const handleDragLeave = useCallback(() => {
    setIsDragActive(false)
  }, [])

  const handleClick = () => {
    if (!disabled) inputRef.current?.click()
  }

  const handleInputChange = (e) => {
    const f = e.target.files[0]
    if (f && validateFile(f)) {
      onFileSelect(f)
    }
    e.target.value = ''
  }

  return (
    <div>
      <div
        id="dropzone"
        className={`dropzone ${isDragActive ? 'dropzone--active' : ''}`}
        onClick={handleClick}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <span className="dropzone__icon">📁</span>
        <p className="dropzone__text">
          <strong>Click to upload</strong> or drag & drop
        </p>
        <p className="dropzone__hint">Supports .csv and .xlsx files (max 10 MB)</p>
        <input
          ref={inputRef}
          type="file"
          className="dropzone__input"
          accept=".csv,.xlsx,.xls"
          onChange={handleInputChange}
          disabled={disabled}
        />
      </div>

      {file && (
        <div className="file-badge">
          <span className="file-badge__icon">📄</span>
          <div className="file-badge__info">
            <div className="file-badge__name">{file.name}</div>
            <div className="file-badge__size">{formatFileSize(file.size)}</div>
          </div>
          {!disabled && (
            <button
              className="file-badge__remove"
              onClick={onRemove}
              title="Remove file"
              type="button"
            >
              ✕
            </button>
          )}
        </div>
      )}
    </div>
  )
}
