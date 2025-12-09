# Game Mode Implementation Guide

This guide explains how to implement **Timed Mode** and **Solo Mode** for TriviaQuest.

## Overview

- **Timed Mode**: Questions have time limits, timer is visible and enforced
- **Solo Mode**: No time limits, timer is hidden, players can take as long as needed

## Implementation Steps

### 1. Add Game Mode State to App.jsx

Add these state variables and import:

```javascript
import GameModeSelection from './components/GameModeSelection'

// Add to state:
const [gameMode, setGameMode] = useState(null) // 'timed' or 'solo' or null

// Add handler:
const handleModeSelect = (mode) => {
  setGameMode(mode)
}
```

### 2. Update App.jsx Flow

Modify the render logic to show mode selection before category selection:

```javascript
// After showHomeScreen check, add:
if (!gameMode) {
  return (
    <div className="app-container">
      <GameModeSelection onSelectMode={handleModeSelect} />
    </div>
  )
}

// Then your existing category selection logic...
if (!selectedCategory) {
  return (
    <CategorySelection
      categories={categories}
      onSelect={handleCategorySelect}
      loading={loading}
    />
  )
}

// Pass gameMode to Quiz:
<Quiz
  category={selectedCategory}
  questions={questions}
  onRestart={handleRestart}
  playerId={playerId}
  gameMode={gameMode}  // Add this prop
/>
```

### 3. Update Quiz.jsx to Handle Modes

Modify the Quiz component to accept and use the gameMode prop:

```javascript
function Quiz({ category, questions, onRestart, playerId, isDailyChallenge = false, onDailyChallengeComplete, gameMode = 'timed' }) {
  // ... existing state ...
  
  // Conditionally set timeLimit based on mode
  const timeLimit = gameMode === 'solo' ? null : (currentQuestion?.time_limit || 30)
  
  // Modify handleTimeUp to only work in timed mode
  const handleTimeUp = () => {
    if (gameMode === 'solo') return // Don't enforce time in solo mode
    setTimeExpired(true)
    // ... rest of existing logic
  }
  
  // In the render, conditionally show Timer:
  return (
    <div className="quiz-container">
      {/* ... existing code ... */}
      
      <div className="quiz-header">
        <h2>{category}</h2>
        {gameMode === 'timed' && (
          <Timer 
            timeLimit={timeLimit} 
            onTimeUp={handleTimeUp}
            isPaused={showFeedback}
          />
        )}
        {gameMode === 'solo' && (
          <div className="mode-badge">Solo Mode - Take Your Time</div>
        )}
        {/* ... rest of header ... */}
      </div>
      
      {/* ... rest of component ... */}
    </div>
  )
}
```

### 4. Update handleRestart to Reset Mode

```javascript
const handleRestart = () => {
  setSelectedCategory(null)
  setQuestions([])
  setGameMode(null) // Reset to mode selection
}
```

### 5. Optional: Add Mode Badge CSS

Add to Quiz.css:

```css
.mode-badge {
  text-align: center;
  padding: 10px 20px;
  background: rgba(0, 102, 204, 0.1);
  color: #0066CC;
  border-radius: 20px;
  font-weight: 600;
  margin: 10px 0;
}

[data-theme="dark"] .mode-badge {
  background: rgba(159, 211, 255, 0.1);
  color: #9fd3ff;
}
```

### 6. Optional: Store Mode Preference

You can save the user's mode preference:

```javascript
const handleModeSelect = (mode) => {
  setGameMode(mode)
  localStorage.setItem('preferredGameMode', mode) // Save preference
}

// Load on mount:
useEffect(() => {
  const savedMode = localStorage.getItem('preferredGameMode')
  if (savedMode) {
    setGameMode(savedMode)
  }
}, [])
```

## Key Differences Between Modes

| Feature | Timed Mode | Solo Mode |
|---------|-----------|-----------|
| Timer Display | ✅ Visible | ❌ Hidden |
| Time Limit | ✅ Enforced | ❌ None |
| Time Expiration | ✅ Auto-submits | ❌ Never expires |
| Time Tracking | ✅ Records time | ✅ Records time (for stats) |
| Hints/Skip | ✅ Disabled when expired | ✅ Always available |

## Testing Checklist

- [ ] Mode selection screen appears after home screen
- [ ] Timed mode shows timer and enforces limits
- [ ] Solo mode hides timer and allows unlimited time
- [ ] Time tracking works in both modes
- [ ] Restart returns to mode selection
- [ ] Mode preference saves/loads (if implemented)
- [ ] Dark mode styling works for mode selection

## Backend Considerations

If you want to track mode in the database:

1. Add `game_mode` column to scores table
2. Update `submitScore` API to accept mode parameter
3. Filter leaderboards by mode if desired

Example API update:
```javascript
export const submitScore = async (playerId, category, score, totalQuestions, timeTaken, hintsUsed, gameMode) => {
  // ... include gameMode in request body
}
```

