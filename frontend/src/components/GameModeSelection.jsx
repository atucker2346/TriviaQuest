import ThemeToggle from './ThemeToggle'
import './GameModeSelection.css'

function GameModeSelection({ onSelectMode }) {
  return (
    <div className="game-mode-selection">
      <div className="mode-selection-header">
        <h2>Choose Your Game Mode</h2>
        <ThemeToggle />
      </div>
      <div className="mode-cards">
        <div 
          className="mode-card"
          onClick={() => onSelectMode('timed')}
        >
          <div className="mode-icon">⏱️</div>
          <h3>Timed Mode</h3>
          <p>Race against the clock! Each question has a time limit. Answer quickly to maximize your score.</p>
          <div className="mode-features">
            <span className="feature-tag">⏰ Time Pressure</span>
            <span className="feature-tag">🏃 Fast Paced</span>
            <span className="feature-tag">⚡ Quick Thinking</span>
          </div>
        </div>
        
        <div 
          className="mode-card"
          onClick={() => onSelectMode('solo')}
        >
          <div className="mode-icon">📚</div>
          <h3>Solo Mode</h3>
          <p>Take your time! No time limits. Perfect for learning and thinking through each question carefully.</p>
          <div className="mode-features">
            <span className="feature-tag">🕐 No Time Limit</span>
            <span className="feature-tag">🧠 Think Deeply</span>
            <span className="feature-tag">📖 Learn Mode</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default GameModeSelection

