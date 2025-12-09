import { useState, useEffect } from 'react'
import { fetchGlobalLeaderboard, fetchPlayerStats, resetLeaderboard, resetAllData } from '../services/api'
import './Scoreboard.css'

function Scoreboard({ playerId, onClose }) {
  const [activeTab, setActiveTab] = useState('global')
  const [leaderboard, setLeaderboard] = useState([])
  const [playerStats, setPlayerStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showResetConfirm, setShowResetConfirm] = useState(false)
  const [resetType, setResetType] = useState(null) // 'scores' or 'all'
  const [resetting, setResetting] = useState(false)

  useEffect(() => {
    loadData()
  }, [activeTab, playerId])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)

      if (activeTab === 'global') {
        const data = await fetchGlobalLeaderboard(100)
        setLeaderboard(data)
      } else if (activeTab === 'mystats' && playerId) {
        const data = await fetchPlayerStats(playerId)
        setPlayerStats(data)
      }
    } catch (err) {
      setError('Failed to load data. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleResetClick = (type) => {
    setResetType(type)
    setShowResetConfirm(true)
  }

  const handleResetConfirm = async () => {
    try {
      setResetting(true)
      setError(null)
      
      if (resetType === 'scores') {
        await resetLeaderboard()
      } else if (resetType === 'all') {
        await resetAllData()
      }
      
      setShowResetConfirm(false)
      setResetType(null)
      
      // Reload data after reset
      await loadData()
      
      alert('Leaderboard reset successfully!')
    } catch (err) {
      setError(err.message || 'Failed to reset leaderboard')
      console.error(err)
    } finally {
      setResetting(false)
    }
  }

  const handleResetCancel = () => {
    setShowResetConfirm(false)
    setResetType(null)
  }

  const renderGlobalLeaderboard = () => {
    if (loading) return <div className="loading">Loading leaderboard...</div>
    if (error) return <div className="error">{error}</div>
    if (leaderboard.length === 0) return <div className="no-data">No scores yet. Be the first!</div>

    return (
      <div className="leaderboard-table-container">
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Player</th>
              <th>Games</th>
              <th>Total Score</th>
              <th>Avg %</th>
              <th>Best %</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry) => (
              <tr 
                key={entry.player_id}
                className={entry.player_id === playerId ? 'current-player' : ''}
              >
                <td className="rank">
                  {entry.rank <= 3 ? (
                    <span className={`medal medal-${entry.rank}`}>
                      {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                    </span>
                  ) : (
                    entry.rank
                  )}
                </td>
                <td className="username">{entry.username}</td>
                <td>{entry.games_played}</td>
                <td>{entry.total_score}/{entry.total_questions}</td>
                <td className="percentage">{entry.avg_percentage}%</td>
                <td className="percentage">{entry.best_percentage}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }

  const renderPlayerStats = () => {
    if (!playerId) {
      return <div className="no-data">Please set a username to view your stats</div>
    }

    if (loading) return <div className="loading">Loading your stats...</div>
    if (error) return <div className="error">{error}</div>
    if (!playerStats) return <div className="no-data">No stats available</div>

    const { player, stats, best_score, recent_scores } = playerStats

    return (
      <div className="player-stats-container">
        <div className="stats-header">
          <h3>{player.username}</h3>
          <p className="member-since">Member since {new Date(player.created_at).toLocaleDateString()}</p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.total_games}</div>
            <div className="stat-label">Games Played</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.total_score}/{stats.total_questions}</div>
            <div className="stat-label">Total Score</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.average_percentage}%</div>
            <div className="stat-label">Average Score</div>
          </div>
        </div>

        {best_score && (
          <div className="best-score-section">
            <h4>🏆 Best Performance</h4>
            <div className="best-score-card">
              <div className="best-score-category">{best_score.category}</div>
              <div className="best-score-result">
                {best_score.score}/{best_score.total_questions} ({best_score.percentage.toFixed(1)}%)
              </div>
              <div className="best-score-date">
                {new Date(best_score.played_at).toLocaleDateString()}
              </div>
            </div>
          </div>
        )}

        {recent_scores && recent_scores.length > 0 && (
          <div className="recent-scores-section">
            <h4>Recent Games</h4>
            <div className="recent-scores-list">
              {recent_scores.map((score, idx) => (
                <div key={idx} className="recent-score-item">
                  <div className="recent-score-category">{score.category}</div>
                  <div className="recent-score-result">
                    {score.score}/{score.total_questions} ({score.percentage.toFixed(1)}%)
                  </div>
                  <div className="recent-score-date">
                    {new Date(score.played_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="scoreboard-overlay">
      <div className="scoreboard-modal">
        <button className="close-button" onClick={onClose}>×</button>
        <div className="scoreboard-header">
          <h2>Scoreboard</h2>
          {activeTab === 'global' && (
            <div className="reset-buttons">
              <button 
                className="reset-button reset-scores"
                onClick={() => handleResetClick('scores')}
                title="Reset all scores (keeps players)"
              >
                🔄 Reset Scores
              </button>
              <button 
                className="reset-button reset-all"
                onClick={() => handleResetClick('all')}
                title="Reset everything (scores + players)"
              >
                ⚠️ Reset All
              </button>
            </div>
          )}
        </div>

        <div className="scoreboard-tabs">
          <button
            className={`tab-button ${activeTab === 'global' ? 'active' : ''}`}
            onClick={() => setActiveTab('global')}
          >
            Global Leaderboard
          </button>
          <button
            className={`tab-button ${activeTab === 'mystats' ? 'active' : ''}`}
            onClick={() => setActiveTab('mystats')}
          >
            My Stats
          </button>
        </div>

        <div className="scoreboard-content">
          {activeTab === 'global' ? renderGlobalLeaderboard() : renderPlayerStats()}
        </div>

        {showResetConfirm && (
          <div className="reset-confirm-overlay">
            <div className="reset-confirm-modal">
              <h3>Confirm Reset</h3>
              <p>
                {resetType === 'scores' 
                  ? 'Are you sure you want to reset all scores? This will clear all leaderboard data but keep player accounts.'
                  : 'Are you sure you want to reset everything? This will delete ALL scores AND ALL player accounts. This action cannot be undone!'}
              </p>
              <div className="reset-confirm-buttons">
                <button 
                  className="confirm-button"
                  onClick={handleResetConfirm}
                  disabled={resetting}
                >
                  {resetting ? 'Resetting...' : 'Yes, Reset'}
                </button>
                <button 
                  className="cancel-button"
                  onClick={handleResetCancel}
                  disabled={resetting}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Scoreboard
