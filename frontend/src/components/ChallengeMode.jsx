import { useState, useEffect } from 'react'
import { fetchCategories, createChallenge, joinChallenge, listChallenges } from '../services/api'
import './ChallengeMode.css'

function ChallengeMode({ playerId, onStartChallenge, onClose }) {
  const [mode, setMode] = useState('select') // 'select', 'create', 'join', 'browse'
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [roomCode, setRoomCode] = useState('')
  const [maxPlayers, setMaxPlayers] = useState(10)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [availableChallenges, setAvailableChallenges] = useState([])

  useEffect(() => {
    loadCategories()
    if (mode === 'browse') {
      loadChallenges()
    }
  }, [mode])

  const loadCategories = async () => {
    try {
      const data = await fetchCategories()
      setCategories(data)
    } catch (err) {
      setError('Failed to load categories')
    }
  }

  const loadChallenges = async () => {
    try {
      setLoading(true)
      const data = await listChallenges()
      setAvailableChallenges(data)
    } catch (err) {
      setError('Failed to load challenges')
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async () => {
    if (!selectedCategory) {
      setError('Please select a category')
      return
    }

    if (!playerId) {
      setError('Please set your username first')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const challenge = await createChallenge(playerId, selectedCategory, maxPlayers)
      onStartChallenge(challenge.challenge_id, challenge.room_code)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleJoin = async () => {
    if (!roomCode.trim()) {
      setError('Please enter a room code')
      return
    }

    if (!playerId) {
      setError('Please set your username first')
      return
    }

    try {
      setLoading(true)
      setError(null)
      const challenge = await joinChallenge(playerId, roomCode.trim())
      onStartChallenge(challenge.challenge_id, challenge.room_code)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleJoinFromList = async (challengeId, roomCode) => {
    if (!playerId) {
      setError('Please set your username first')
      return
    }

    try {
      setLoading(true)
      setError(null)
      await joinChallenge(playerId, roomCode)
      onStartChallenge(challengeId, roomCode)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (mode === 'create') {
    return (
      <div className="challenge-mode">
        <div className="challenge-header">
          <button onClick={() => setMode('select')} className="back-btn">← Back</button>
          <h2>Create Challenge</h2>
        </div>
        <div className="challenge-content">
          <div className="form-group">
            <label>Select Category</label>
            <div className="categories-grid">
              {categories.map((cat) => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label>Max Players: {maxPlayers}</label>
            <input
              type="range"
              min="2"
              max="20"
              value={maxPlayers}
              onChange={(e) => setMaxPlayers(parseInt(e.target.value))}
              className="slider"
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button onClick={handleCreate} disabled={loading || !selectedCategory} className="create-btn">
            {loading ? 'Creating...' : 'Create Challenge'}
          </button>
        </div>
      </div>
    )
  }

  if (mode === 'join') {
    return (
      <div className="challenge-mode">
        <div className="challenge-header">
          <button onClick={() => setMode('select')} className="back-btn">← Back</button>
          <h2>Join Challenge</h2>
        </div>
        <div className="challenge-content">
          <div className="form-group">
            <label>Enter Room Code</label>
            <input
              type="text"
              value={roomCode}
              onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
              placeholder="ABC123"
              maxLength="6"
              className="room-code-input"
            />
          </div>
          {error && <div className="error-message">{error}</div>}
          <button onClick={handleJoin} disabled={loading || !roomCode.trim()} className="join-btn">
            {loading ? 'Joining...' : 'Join Challenge'}
          </button>
        </div>
      </div>
    )
  }

  if (mode === 'browse') {
    return (
      <div className="challenge-mode">
        <div className="challenge-header">
          <button onClick={() => setMode('select')} className="back-btn">← Back</button>
          <h2>Browse Challenges</h2>
        </div>
        <div className="challenge-content">
          {loading ? (
            <div className="loading">Loading challenges...</div>
          ) : availableChallenges.length === 0 ? (
            <div className="no-challenges">No available challenges. Create one to get started!</div>
          ) : (
            <div className="challenges-list">
              {availableChallenges.map((challenge) => (
                <div key={challenge.id} className="challenge-item">
                  <div className="challenge-info">
                    <div className="challenge-category">{challenge.category}</div>
                    <div className="challenge-code">Room: {challenge.room_code}</div>
                    <div className="challenge-players">
                      {challenge.participant_count}/{challenge.max_players} players
                    </div>
                    <div className="challenge-creator">by {challenge.creator_name}</div>
                  </div>
                  <button
                    onClick={() => handleJoinFromList(challenge.id, challenge.room_code)}
                    disabled={loading}
                    className="join-item-btn"
                  >
                    Join
                  </button>
                </div>
              ))}
            </div>
          )}
          {error && <div className="error-message">{error}</div>}
        </div>
      </div>
    )
  }

  return (
    <div className="challenge-mode">
      <div className="challenge-header">
        <button onClick={onClose} className="close-btn">×</button>
        <h2>Challenge Mode</h2>
      </div>
      <div className="challenge-content">
        <p className="challenge-description">
          Compete with friends or players worldwide in real-time trivia challenges!
        </p>
        <div className="mode-buttons">
          <button onClick={() => setMode('create')} className="mode-btn create-mode">
            <span className="mode-icon">➕</span>
            <span className="mode-title">Create Challenge</span>
            <span className="mode-desc">Start a new challenge room</span>
          </button>
          <button onClick={() => setMode('join')} className="mode-btn join-mode">
            <span className="mode-icon">🔗</span>
            <span className="mode-title">Join by Code</span>
            <span className="mode-desc">Enter a room code</span>
          </button>
          <button onClick={() => setMode('browse')} className="mode-btn browse-mode">
            <span className="mode-icon">🌍</span>
            <span className="mode-title">Browse Global</span>
            <span className="mode-desc">Find public challenges</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChallengeMode

