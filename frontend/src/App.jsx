import { useState, useEffect } from 'react'
import { fetchCategories, fetchQuestions, registerPlayer } from './services/api'
import HomeScreen from './components/HomeScreen'
import GameModeSelection from './components/GameModeSelection'
import CategorySelection from './components/CategorySelection'
import Quiz from './components/Quiz'
import PlayerSetup from './components/PlayerSetup'
import Scoreboard from './components/Scoreboard'
import DailyChallenge from './components/DailyChallenge'
import ChallengeMode from './components/ChallengeMode'
import ChallengeRoom from './components/ChallengeRoom'
import ThemeToggle from './components/ThemeToggle'
import SoundToggle from './components/SoundToggle'
import './App.css'

function App() {
  const [showHomeScreen, setShowHomeScreen] = useState(true)
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [playerId, setPlayerId] = useState(null)
  const [playerUsername, setPlayerUsername] = useState(null)
  const [showPlayerSetup, setShowPlayerSetup] = useState(false)
  const [showScoreboard, setShowScoreboard] = useState(false)
  const [showDailyChallenge, setShowDailyChallenge] = useState(false)
  const [showChallengeMode, setShowChallengeMode] = useState(false)
  const [currentChallenge, setCurrentChallenge] = useState(null)
  const [gameMode, setGameMode] = useState(null) // 'timed' or 'solo' or null

  useEffect(() => {
    loadCategories()
    loadPlayerFromStorage()
  }, [])

  const loadPlayerFromStorage = () => {
    const storedPlayerId = localStorage.getItem('playerId')
    const storedUsername = localStorage.getItem('playerUsername')
    if (storedPlayerId && storedUsername) {
      setPlayerId(parseInt(storedPlayerId))
      setPlayerUsername(storedUsername)
    }
  }

  const loadCategories = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchCategories()
      setCategories(data)
    } catch (err) {
      setError('Failed to load categories. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCategorySelect = async (category) => {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchQuestions(category)
      setQuestions(data)
      setSelectedCategory(category)
    } catch (err) {
      setError('Failed to load questions. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRestart = () => {
    setSelectedCategory(null)
    setQuestions([])
    setGameMode(null) // Reset to mode selection
    setShowChallengeMode(false) // Close challenge mode if open
    setCurrentChallenge(null) // Clear any challenge state
  }

  const handleModeSelect = (mode) => {
    if (mode === 'challenge') {
      setShowChallengeMode(true)
    } else {
      setGameMode(mode)
      setShowChallengeMode(false) // Ensure challenge mode is closed when selecting other modes
    }
  }

  const handleStartGame = () => {
    setShowHomeScreen(false)
  }

  const handleSetPlayer = async (username) => {
    if (!username) {
      // User skipped
      setShowPlayerSetup(false)
      return
    }

    try {
      const data = await registerPlayer(username)
      setPlayerId(data.player_id)
      setPlayerUsername(data.username)
      localStorage.setItem('playerId', data.player_id.toString())
      localStorage.setItem('playerUsername', data.username)
      setShowPlayerSetup(false)
    } catch (err) {
      alert('Failed to register player: ' + err.message)
    }
  }

  const handleLogout = () => {
    setPlayerId(null)
    setPlayerUsername(null)
    localStorage.removeItem('playerId')
    localStorage.removeItem('playerUsername')
  }

  if (showHomeScreen) {
    return <HomeScreen onStart={handleStartGame} />
  }

  // Show mode selection before category selection
  if (!gameMode) {
    return (
      <div className="app-container">
        <GameModeSelection onSelectMode={handleModeSelect} />
        {showChallengeMode && !currentChallenge && (
          <ChallengeMode
            playerId={playerId}
            onStartChallenge={(challengeId, roomCode) => {
              setCurrentChallenge({ challengeId, roomCode })
              setShowChallengeMode(false)
            }}
            onClose={() => setShowChallengeMode(false)}
          />
        )}
        {currentChallenge && (
          <ChallengeRoom
            challengeId={currentChallenge.challengeId}
            roomCode={currentChallenge.roomCode}
            playerId={playerId}
            onClose={() => {
              setCurrentChallenge(null)
              setShowChallengeMode(false)
            }}
            onComplete={() => {
              // Challenge completed, keep room open to see final results
            }}
          />
        )}
      </div>
    )
  }

  if (loading && !selectedCategory) {
    return (
      <div className="app-container">
        <div className="loading">Loading categories...</div>
      </div>
    )
  }

  if (error && !selectedCategory) {
    return (
      <div className="app-container">
        <div className="error">{error}</div>
        <button onClick={loadCategories} className="retry-button">
          Retry
        </button>
      </div>
    )
  }

  if (showPlayerSetup) {
    return (
      <div className="app-container">
        <h1 className="app-title">TriviaQuest</h1>
        <PlayerSetup onSetPlayer={handleSetPlayer} />
      </div>
    )
  }

  return (
    <div className="app-container">
      <div className="app-header">
        <h1 className="app-title">TriviaQuest</h1>
        <div className="app-controls">
          <ThemeToggle />
          <SoundToggle />
          <button 
            className="daily-challenge-button"
            onClick={() => setShowDailyChallenge(true)}
            title="Daily Challenge"
          >
            📅 Daily
          </button>
          <button 
            className="scoreboard-button"
            onClick={() => setShowScoreboard(true)}
          >
            🏆 Leaderboard
          </button>
          {playerUsername ? (
            <div className="player-info">
              <span className="player-name">👤 {playerUsername}</span>
              <button 
                className="logout-button"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          ) : (
            <button 
              className="login-button"
              onClick={() => setShowPlayerSetup(true)}
            >
              Set Username
            </button>
          )}
        </div>
      </div>

      {!selectedCategory ? (
        <CategorySelection
          categories={categories}
          onSelect={handleCategorySelect}
          loading={loading}
        />
      ) : (
        <Quiz
          category={selectedCategory}
          questions={questions}
          onRestart={handleRestart}
          playerId={playerId}
          gameMode={gameMode}
        />
      )}

      {showScoreboard && (
        <Scoreboard
          playerId={playerId}
          onClose={() => setShowScoreboard(false)}
        />
      )}

      {showDailyChallenge && (
        <DailyChallenge
          playerId={playerId}
          onClose={() => setShowDailyChallenge(false)}
        />
      )}
    </div>
  )
}

export default App
