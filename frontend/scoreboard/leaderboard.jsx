import React, { useState, useEffect } from 'react';
import './Leaderboard.css';

const Leaderboard = () => {
  const [activeTab, setActiveTab] = useState('global');
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Fetch leaderboard data when tab or category changes
  useEffect(() => {
    fetchLeaderboard();
  }, [activeTab, selectedCategory]);

  const fetchCategories = async () => {
    try {
      const response = await fetch('http://localhost:5001/categories');
      const data = await response.json();
      setCategories(data);
    } catch (err) {
      console.error('Failed to fetch categories:', err);
    }
  };

  const fetchLeaderboard = async () => {
    setLoading(true);
    setError(null);
    
    try {
      let url = 'http://localhost:5001/leaderboard/';
      
      if (activeTab === 'category' && selectedCategory) {
        url += `category/${encodeURIComponent(selectedCategory)}`;
      } else if (activeTab === 'category' && !selectedCategory) {
        setLoading(false);
        setLeaderboardData([]);
        return;
      } else {
        url += activeTab;
      }
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error('Failed to fetch leaderboard');
      }
      
      const data = await response.json();
      setLeaderboardData(data);
    } catch (err) {
      setError(err.message);
      setLeaderboardData([]);
    } finally {
      setLoading(false);
    }
  };

  const getRankIcon = (rank) => {
    switch(rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return rank;
    }
  };

  const handleCategoryChange = (e) => {
    setSelectedCategory(e.target.value);
  };

  return (
    <div className="leaderboard-container">
      <h1 className="leaderboard-title">🏆 Leaderboard</h1>
      
      <div className="leaderboard-tabs">
        <button
          className={`tab-button ${activeTab === 'global' ? 'active' : ''}`}
          onClick={() => setActiveTab('global')}
        >
          🌍 Global
        </button>
        <button
          className={`tab-button ${activeTab === 'daily' ? 'active' : ''}`}
          onClick={() => setActiveTab('daily')}
        >
          📅 Daily
        </button>
        <button
          className={`tab-button ${activeTab === 'weekly' ? 'active' : ''}`}
          onClick={() => setActiveTab('weekly')}
        >
          📊 Weekly
        </button>
        <button
          className={`tab-button ${activeTab === 'category' ? 'active' : ''}`}
          onClick={() => setActiveTab('category')}
        >
          📚 By Category
        </button>
      </div>

      {activeTab === 'category' && (
        <div className="category-selector">
          <label htmlFor="category-select">Select Category:</label>
          <select
            id="category-select"
            value={selectedCategory}
            onChange={handleCategoryChange}
            className="category-dropdown"
          >
            <option value="">-- Choose a category --</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="leaderboard-content">
        {loading && <div className="loading">Loading leaderboard...</div>}
        
        {error && <div className="error">Error: {error}</div>}
        
        {!loading && !error && leaderboardData.length === 0 && (
          <div className="no-data">
            {activeTab === 'category' && !selectedCategory
              ? 'Please select a category to view the leaderboard'
              : 'No data available yet. Be the first to play!'}
          </div>
        )}
        
        {!loading && !error && leaderboardData.length > 0 && (
          <div className="leaderboard-table-wrapper">
            <table className="leaderboard-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Player</th>
                  <th>Games</th>
                  <th>Total Score</th>
                  <th>Avg Score</th>
                  <th>Best Score</th>
                  <th>Accuracy</th>
                </tr>
              </thead>
              <tbody>
                {leaderboardData.map((player) => (
                  <tr key={player.rank} className={player.rank <= 3 ? 'top-three' : ''}>
                    <td className="rank-cell">
                      <span className="rank-badge">{getRankIcon(player.rank)}</span>
                    </td>
                    <td className="username-cell">{player.username}</td>
                    <td>{player.games_played}</td>
                    <td className="score-cell">{player.total_score}</td>
                    <td>{player.avg_score}</td>
                    <td className="best-score-cell">{player.best_score}</td>
                    <td className="accuracy-cell">{player.accuracy}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Leaderboard;
