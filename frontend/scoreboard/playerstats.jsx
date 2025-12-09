import React, { useState, useEffect } from 'react';
import './PlayerStats.css';

const PlayerStats = ({ username }) => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchUsername, setSearchUsername] = useState(username || '');

  useEffect(() => {
    if (username) {
      fetchPlayerStats(username);
    }
  }, [username]);

  const fetchPlayerStats = async (playerUsername) => {
    if (!playerUsername.trim()) {
      setError('Please enter a username');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `http://localhost:5001/player/${encodeURIComponent(playerUsername)}/stats`
      );
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Player not found');
        }
        throw new Error('Failed to fetch player stats');
      }
      
      const data = await response.json();
      setStats(data);
    } catch (err) {
      setError(err.message);
      setStats(null);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchPlayerStats(searchUsername);
  };

  return (
    <div className="player-stats-container">
      <h1 className="stats-title">📊 Player Statistics</h1>
      
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={searchUsername}
          onChange={(e) => setSearchUsername(e.target.value)}
          placeholder="Enter username..."
          className="search-input"
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>

      {loading && <div className="loading">Loading player stats...</div>}
      
      {error && <div className="error">Error: {error}</div>}
      
      {!loading && !error && stats && (
        <div className="stats-content">
          <div className="player-header">
            <h2 className="player-name">{stats.username}</h2>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">🎮</div>
              <div className="stat-value">{stats.overall.total_games}</div>
              <div className="stat-label">Total Games</div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">⭐</div>
              <div className="stat-value">{stats.overall.total_score}</div>
              <div className="stat-label">Total Score</div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">📈</div>
              <div className="stat-value">{stats.overall.avg_score}</div>
              <div className="stat-label">Average Score</div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🏆</div>
              <div className="stat-value">{stats.overall.best_score}</div>
              <div className="stat-label">Best Score</div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">🎯</div>
              <div className="stat-value">{stats.overall.accuracy}%</div>
              <div className="stat-label">Accuracy</div>
            </div>

            {stats.overall.avg_time && (
              <div className="stat-card">
                <div className="stat-icon">⏱️</div>
                <div className="stat-value">{stats.overall.avg_time}s</div>
                <div className="stat-label">Avg Time</div>
              </div>
            )}
          </div>

          {stats.by_category && stats.by_category.length > 0 && (
            <div className="category-stats">
              <h3 className="section-title">Performance by Category</h3>
              <div className="category-grid">
                {stats.by_category.map((cat) => (
                  <div key={cat.category} className="category-card">
                    <h4 className="category-name">{cat.category}</h4>
                    <div className="category-details">
                      <div className="category-stat">
                        <span className="label">Games:</span>
                        <span className="value">{cat.games_played}</span>
                      </div>
                      <div className="category-stat">
                        <span className="label">Avg Score:</span>
                        <span className="value">{cat.avg_score}</span>
                      </div>
                      <div className="category-stat">
                        <span className="label">Best:</span>
                        <span className="value highlight">{cat.best_score}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {stats.recent_games && stats.recent_games.length > 0 && (
            <div className="recent-games">
              <h3 className="section-title">Recent Games</h3>
              <div className="games-table-wrapper">
                <table className="games-table">
                  <thead>
                    <tr>
                      <th>Category</th>
                      <th>Score</th>
                      <th>Correct</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.recent_games.map((game, idx) => (
                      <tr key={idx}>
                        <td>{game.category || 'Mixed'}</td>
                        <td className="score-cell">{game.score}</td>
                        <td>{game.correct}/{game.total}</td>
                        <td className="date-cell">
                          {new Date(game.played_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {!loading && !error && !stats && (
        <div className="no-data">
          Enter a username to view player statistics
        </div>
      )}
    </div>
  );
};

export default PlayerStats;
