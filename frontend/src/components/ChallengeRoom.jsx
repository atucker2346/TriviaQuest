import { useState, useEffect } from 'react'
import Quiz from './Quiz'
import { getChallenge, startChallenge, getChallengeLeaderboard, submitChallengeScore } from '../services/api'
import './ChallengeRoom.css'

function ChallengeRoom({ challengeId, roomCode, playerId, onClose, onComplete }) {
  const [challenge, setChallenge] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showQuiz, setShowQuiz] = useState(false)
  const [isCreator, setIsCreator] = useState(false)
  const [pollingInterval, setPollingInterval] = useState(null)

  useEffect(() => {
    loadChallenge()
  }, [challengeId])

  useEffect(() => {
    if (challenge?.status === 'active') {
      setShowQuiz(true)
      const interval = setInterval(() => {
        loadChallenge()
        loadLeaderboard()
      }, 2000) // Poll every 2 seconds
      setPollingInterval(interval)
      return () => clearInterval(interval)
    } else if (challenge?.status === 'waiting') {
      const interval = setInterval(() => {
        loadChallenge()
      }, 3000) // Poll every 3 seconds while waiting
      setPollingInterval(interval)
      return () => clearInterval(interval)
    }
  }, [challenge?.status])

  const loadChallenge = async () => {
    try {
      setError(null)
      const data = await getChallenge(challengeId)
      setChallenge(data)
      const creator = data.participants.find(p => p.id === playerId)
      setIsCreator(creator && creator.id === data.participants[0]?.id)
      
      if (data.status === 'active' && !showQuiz) {
        setShowQuiz(true)
        loadLeaderboard()
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadLeaderboard = async () => {
    try {
      const data = await getChallengeLeaderboard(challengeId)
      setLeaderboard(data)
    } catch (err) {
      console.error('Failed to load leaderboard:', err)
    }
  }

  const handleStart = async () => {
    if (!playerId) {
      setError('Please set your username first')
      return
    }

    try {
      setLoading(true)
      await startChallenge(challengeId, playerId)
      await loadChallenge()
      setShowQuiz(true)
      loadLeaderboard()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleQuizComplete = async (score, totalQuestions, timeTaken) => {
    try {
      await submitChallengeScore(challengeId, playerId, score, totalQuestions, timeTaken)
      // Continue polling to see final results
      await loadChallenge()
      await loadLeaderboard()
    } catch (err) {
      console.error('Failed to submit score:', err)
      setError('Failed to submit score: ' + err.message)
    }
  }

  if (loading && !challenge) {
    return (
      <div className="challenge-room-overlay">
        <div className="challenge-room-modal">
          <div className="loading">Loading challenge...</div>
        </div>
      </div>
    )
  }

  if (error && !challenge) {
    return (
      <div className="challenge-room-overlay">
        <div className="challenge-room-modal">
          <div className="error">{error}</div>
          <button onClick={onClose} className="close-btn">Close</button>
        </div>
      </div>
    )
  }

  if (showQuiz && challenge) {
    return (
      <div className="challenge-room-overlay">
        <div className="challenge-room-modal quiz-modal">
          <div className="challenge-room-header">
            <div className="room-info">
              <div className="room-code-display">Room: {roomCode}</div>
              <div className="room-category">{challenge.category}</div>
            </div>
            <button onClick={onClose} className="close-btn">×</button>
          </div>
          <div className="challenge-content-wrapper">
            <div className="quiz-section">
              <Quiz
                category={`Challenge - ${challenge.category}`}
                questions={challenge.questions}
                onRestart={() => {}}
                playerId={playerId}
                isDailyChallenge={false}
                onDailyChallengeComplete={handleQuizComplete}
              />
            </div>
            <div className="leaderboard-section">
              <h3>Live Leaderboard</h3>
              <div className="leaderboard-list">
                {leaderboard.length === 0 ? (
                  <div className="no-scores">No scores yet</div>
                ) : (
                  leaderboard.map((entry) => (
                    <div
                      key={entry.player_id}
                      className={`leaderboard-entry ${entry.player_id === playerId ? 'current-player' : ''} ${entry.status === 'completed' ? 'completed' : ''}`}
                    >
                      <div className="entry-rank">
                        {entry.rank <= 3 ? (
                          <span className="medal">
                            {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                          </span>
                        ) : (
                          `#${entry.rank}`
                        )}
                      </div>
                      <div className="entry-name">{entry.username}</div>
                      <div className="entry-score">
                        {entry.status === 'completed' ? (
                          <>
                            {entry.score}/{entry.total_questions} ({entry.percentage}%)
                            {entry.time_taken && <span className="entry-time">⏱️ {entry.time_taken}s</span>}
                          </>
                        ) : (
                          <span className="playing">Playing...</span>
                        )}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="challenge-room-overlay">
      <div className="challenge-room-modal">
        <div className="challenge-room-header">
          <h2>Challenge Room</h2>
          <button onClick={onClose} className="close-btn">×</button>
        </div>
        <div className="challenge-room-content">
          <div className="room-code-section">
            <div className="room-code-label">Room Code</div>
            <div className="room-code-large">{roomCode}</div>
            <p className="share-text">Share this code with friends to join!</p>
          </div>

          <div className="room-details">
            <div className="detail-item">
              <span className="detail-label">Category:</span>
              <span className="detail-value">{challenge?.category}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Players:</span>
              <span className="detail-value">
                {challenge?.participants.length || 0}/{challenge?.max_players || 10}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Status:</span>
              <span className="detail-value">{challenge?.status || 'waiting'}</span>
            </div>
          </div>

          <div className="participants-list">
            <h3>Participants</h3>
            {challenge?.participants.map((p) => (
              <div key={p.id} className={`participant ${p.id === playerId ? 'you' : ''}`}>
                <span className="participant-name">{p.username}</span>
                {p.id === playerId && <span className="you-badge">You</span>}
                {p.status === 'completed' && <span className="completed-badge">✓ Done</span>}
              </div>
            ))}
          </div>

          {error && <div className="error-message">{error}</div>}

          {challenge?.status === 'waiting' && isCreator && (
            <button onClick={handleStart} disabled={loading} className="start-challenge-btn">
              {loading ? 'Starting...' : 'Start Challenge'}
            </button>
          )}

          {challenge?.status === 'waiting' && !isCreator && (
            <div className="waiting-message">Waiting for host to start the challenge...</div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ChallengeRoom

