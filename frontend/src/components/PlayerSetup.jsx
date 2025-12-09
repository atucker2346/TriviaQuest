import { useState } from 'react'
import './PlayerSetup.css'

function PlayerSetup({ onSetPlayer }) {
  const [username, setUsername] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const trimmedUsername = username.trim()
    
    if (trimmedUsername.length < 3) {
      setError('Username must be at least 3 characters')
      return
    }
    
    if (trimmedUsername.length > 20) {
      setError('Username must be less than 20 characters')
      return
    }
    
    onSetPlayer(trimmedUsername)
  }

  return (
    <div className="player-setup">
      <h3>Enter Your Username</h3>
      <p className="player-setup-description">
        Track your scores and compete on the global leaderboard!
      </p>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={username}
          onChange={(e) => {
            setUsername(e.target.value)
            setError('')
          }}
          placeholder="Your username"
          className="username-input"
          maxLength={20}
        />
        {error && <div className="error-message">{error}</div>}
        <button type="submit" className="submit-button">
          Continue
        </button>
      </form>
      <button 
        className="skip-button"
        onClick={() => onSetPlayer(null)}
      >
        Skip for now
      </button>
    </div>
  )
}

export default PlayerSetup
