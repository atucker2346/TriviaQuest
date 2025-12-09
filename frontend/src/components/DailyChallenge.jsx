import { useState, useEffect } from 'react'
import { getTodayChallenge, submitDailyChallenge, getDailyLeaderboard, getPlayerStreak } from '../services/api'
import Quiz from './Quiz'
import './DailyChallenge.css'

function DailyChallenge({ playerId, onClose }) {
  const [challenge, setChallenge] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [streak, setStreak] = useState(null)
  const [leaderboard, setLeaderboard] = useState([])
  const [showQuiz, setShowQuiz] = useState(false)
  const [showLeaderboard, setShowLeaderboard] = useState(false)
  const [completionMessage, setCompletionMessage] = useState(null)

  useEffect(() => {
    loadChallenge()
    if (playerId) {
      loadStreak()
    }
  }, [playerId])

  const loadChallenge = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getTodayChallenge()
      setChallenge(data)
    } catch (err) {
      setError('Failed to load daily challenge: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const loadStreak = async () => {
    try {
      const data = await getPlayerStreak(playerId)
      setStreak(data)
    } catch (err) {
      console.error('Failed to load streak:', err)
    }
  }

  const loadLeaderboard = async () => {
    try {
      const data = await getDailyLeaderboard(50)
      setLeaderboard(data)
      setShowLeaderboard(true)
    } catch (err) {
      console.error('Failed to load leaderboard:', err)
    }
  }

  const handleStartChallenge = () => {
    if (!playerId) {
      alert('Please set your username first!')
      onClose()
      return
    }
    
    if (streak?.completed_today) {
      alert('You have already completed today\'s challenge!')
      return
    }
    
    setShowQuiz(true)
  }

  const handleChallengeComplete = async (score, totalQuestions, timeTaken) => {
    try {
      const result = await submitDailyChallenge(
        challenge.challenge_id,
        playerId,
        score,
        totalQuestions,
        timeTaken
      )
      
      setCompletionMessage({
        score,
        totalQuestions,
        currentStreak: result.current_streak,
        longestStreak: result.longest_streak
      })
      
      // Reload streak
      await loadStreak()
    } catch (err) {
      alert('Failed to submit challenge: ' + err.message)
    }
  }

  const handleBackToMenu = () => {
    setShowQuiz(false)
    setCompletionMessage(null)
  }

  if (loading) {
    return (
      <div className="daily-challenge-overlay">
        <div className="daily-challenge-modal">
          <div className="loading">Loading daily challenge...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="daily-challenge-overlay">
        <div className="daily-challenge-modal">
          <div className="error">{error}</div>
          <button onClick={onClose} className="close-button">Close</button>
        </div>
      </div>
    )
  }

  if (showQuiz && challenge) {
    return (
      <div className="daily-challenge-overlay">
        <div className="daily-challenge-modal quiz-modal">
          <button onClick={handleBackToMenu} className="close-button-x">✕</button>
          <Quiz
            category={`Daily Challenge - ${challenge.category}`}
            questions={challenge.questions}
            onRestart={handleBackToMenu}
            playerId={playerId}
            isDailyChallenge={true}
            onDailyChallengeComplete={handleChallengeComplete}
          />
        </div>
      </div>
    )
  }

  if (completionMessage) {
    const percentage = Math.round((completionMessage.score / completionMessage.totalQuestions) * 100)
    return (
      <div className="daily-challenge-overlay">
        <div className="daily-challenge-modal">
          <h2>🎉 Daily Challenge Complete!</h2>
          <div className="completion-stats">
            <div className="completion-score">
              <span className="score-big">{completionMessage.score}/{completionMessage.totalQuestions}</span>
              <span className="percentage">{percentage}%</span>
            </div>
            <div className="streak-info">
              <div className="streak-item">
                <span className="streak-emoji">🔥</span>
                <div>
                  <div className="streak-label">Current Streak</div>
                  <div className="streak-value">{completionMessage.currentStreak} days</div>
                </div>
              </div>
              <div className="streak-item">
                <span className="streak-emoji">🏆</span>
                <div>
                  <div className="streak-label">Longest Streak</div>
                  <div className="streak-value">{completionMessage.longestStreak} days</div>
                </div>
              </div>
            </div>
          </div>
          <div className="completion-message">
            Come back tomorrow for a new challenge!
          </div>
          <div className="modal-actions">
            <button onClick={loadLeaderboard} className="leaderboard-btn">
              View Leaderboard
            </button>
            <button onClick={onClose} className="close-button">
              Close
            </button>
          </div>
        </div>
      </div>
    )
  }

  if (showLeaderboard) {
    return (
      <div className="daily-challenge-overlay">
        <div className="daily-challenge-modal">
          <h2>🏆 Today's Leaderboard</h2>
          <div className="leaderboard-list">
            {leaderboard.length === 0 ? (
              <p className="no-data">No scores yet today. Be the first!</p>
            ) : (
              leaderboard.map((entry) => (
                <div key={entry.rank} className={`leaderboard-entry ${entry.player_id === playerId ? 'current-player' : ''}`}>
                  <span className="rank">#{entry.rank}</span>
                  <span className="username">{entry.username}</span>
                  <span className="score">{entry.score}/{entry.total_questions}</span>
                  <span className="percentage">{entry.percentage}%</span>
                  <span className="time">⏱️ {entry.time_taken}s</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="daily-challenge-overlay">
      <div className="daily-challenge-modal">
        <button onClick={onClose} className="close-button-x">✕</button>
        <h2>📅 Daily Challenge</h2>
        <div className="challenge-date">
          {new Date().toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
          })}
        </div>
        
        {challenge && (
          <div className="challenge-info">
            <div className="challenge-category">
              <span className="label">Category:</span>
              <span className="value">{challenge.category}</span>
            </div>
            <div className="challenge-questions">
              <span className="label">Questions:</span>
              <span className="value">{challenge.questions.length}</span>
            </div>
          </div>
        )}

        {streak && (
          <div className="streak-display">
            <div className="streak-card">
              <span className="streak-emoji">🔥</span>
              <div className="streak-details">
                <div className="streak-number">{streak.current_streak}</div>
                <div className="streak-text">Day Streak</div>
              </div>
            </div>
            <div className="streak-card">
              <span className="streak-emoji">🏆</span>
              <div className="streak-details">
                <div className="streak-number">{streak.longest_streak}</div>
                <div className="streak-text">Best Streak</div>
              </div>
            </div>
          </div>
        )}

        {streak?.completed_today ? (
          <div className="already-completed">
            <div className="completed-icon">✓</div>
            <div className="completed-text">Challenge completed today!</div>
            <div className="completed-subtext">Come back tomorrow for a new challenge</div>
          </div>
        ) : (
          <button onClick={handleStartChallenge} className="start-challenge-button">
            Start Challenge
          </button>
        )}

        <button onClick={loadLeaderboard} className="view-leaderboard-button">
          View Today's Leaderboard
        </button>
      </div>
    </div>
  )
}

export default DailyChallenge
