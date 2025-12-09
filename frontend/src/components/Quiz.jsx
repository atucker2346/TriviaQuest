import { useState, useEffect } from 'react'
import Question from './Question'
import AnswerFeedback from './AnswerFeedback'
import Timer from './Timer'
import { submitScore } from '../services/api'
import './Quiz.css'

function Quiz({ category, questions, onRestart, playerId, isDailyChallenge = false, onDailyChallengeComplete, gameMode = 'timed' }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [showResults, setShowResults] = useState(false)
  const [showFeedback, setShowFeedback] = useState(false)
  const [isAnswerCorrect, setIsAnswerCorrect] = useState(false)
  const [scoreSubmitted, setScoreSubmitted] = useState(false)
  const [questionStartTime, setQuestionStartTime] = useState(Date.now())
  const [totalTimeTaken, setTotalTimeTaken] = useState(0)
  const [questionTimes, setQuestionTimes] = useState({})
  const [hintsUsed, setHintsUsed] = useState(0)
  const [usedFiftyFifty, setUsedFiftyFifty] = useState({})
  const [skippedQuestions, setSkippedQuestions] = useState({})
  const [eliminatedChoices, setEliminatedChoices] = useState({})
  const [timeExpired, setTimeExpired] = useState(false)

  const currentQuestion = questions[currentQuestionIndex]
  const totalQuestions = questions.length
  const timeLimit = gameMode === 'solo' ? null : (currentQuestion?.time_limit || 30)

  useEffect(() => {
    setQuestionStartTime(Date.now())
    setTimeExpired(false)
  }, [currentQuestionIndex])

  const handleAnswerSelect = (answer) => {
    if (gameMode === 'timed' && timeExpired) return
    setSelectedAnswers({
      ...selectedAnswers,
      [currentQuestionIndex]: answer,
    })
  }

  const handleTimeUp = () => {
    if (gameMode === 'solo') return // Don't enforce time in solo mode
    setTimeExpired(true)
    
    // Record time for current question
    const timeTaken = Math.floor((Date.now() - questionStartTime) / 1000)
    const updatedQuestionTimes = {
      ...questionTimes,
      [currentQuestionIndex]: timeTaken
    }
    setQuestionTimes(updatedQuestionTimes)
    
    // End the quiz immediately - calculate final score and show results
    const finalScore = calculateScore()
    // Calculate total time including current question
    const previousTotalTime = Object.values(questionTimes).reduce((sum, time) => sum + time, 0)
    const finalTime = previousTotalTime + timeTaken
    setScore(finalScore)
    setTotalTimeTaken(finalTime)
    setShowResults(true)

    if (playerId && !scoreSubmitted) {
      try {
        if (isDailyChallenge && onDailyChallengeComplete) {
          await onDailyChallengeComplete(finalScore, totalQuestions, finalTime)
        } else {
          await submitScore(playerId, category, finalScore, totalQuestions, finalTime, hintsUsed)
        }
        setScoreSubmitted(true)
      } catch (error) {
        console.error('Failed to submit score:', error)
      }
    }
  }

  const handleFiftyFifty = () => {
    if (usedFiftyFifty[currentQuestionIndex]) return

    const correctAnswer = currentQuestion.correct_answer
    const incorrectChoices = currentQuestion.choices.filter(c => c !== correctAnswer)
    
    // Randomly select 2 incorrect choices to eliminate
    const shuffled = [...incorrectChoices].sort(() => Math.random() - 0.5)
    const toEliminate = shuffled.slice(0, 2)
    
    setEliminatedChoices({
      ...eliminatedChoices,
      [currentQuestionIndex]: toEliminate
    })
    
    setUsedFiftyFifty({
      ...usedFiftyFifty,
      [currentQuestionIndex]: true
    })
    
    setHintsUsed(hintsUsed + 1)
  }

  const handleSkip = () => {
    if (skippedQuestions[currentQuestionIndex]) return
    
    setSkippedQuestions({
      ...skippedQuestions,
      [currentQuestionIndex]: true
    })
    
    setHintsUsed(hintsUsed + 1)
    
    // Move to next question
    handleContinue()
  }

  const handleNext = () => {
    if (gameMode === 'timed' && timeExpired) return

    const selectedAnswer = selectedAnswers[currentQuestionIndex]

    if (!selectedAnswer && !skippedQuestions[currentQuestionIndex]) {
      alert('Please select an answer, use a hint, or skip the question')
      return
    }

    // Record time for this question
    const timeTaken = Math.floor((Date.now() - questionStartTime) / 1000)
    setQuestionTimes({
      ...questionTimes,
      [currentQuestionIndex]: timeTaken
    })

    const isCorrect = selectedAnswer === currentQuestion.correct_answer
    setIsAnswerCorrect(isCorrect)

    if (isCorrect) {
      setScore(score + 1)
    }

    setShowFeedback(true)
  }

  const handleContinue = async () => {
    setShowFeedback(false)
    setTimeExpired(false)

    const isLastQuestion = currentQuestionIndex >= totalQuestions - 1

    if (isLastQuestion) {
      const finalScore = calculateScore()
      const finalTime = calculateTotalTime()
      setScore(finalScore)
      setTotalTimeTaken(finalTime)
      setShowResults(true)

      if (playerId && !scoreSubmitted) {
        try {
          if (onDailyChallengeComplete) {
            // Used for both daily challenges and regular challenges
            await onDailyChallengeComplete(finalScore, totalQuestions, finalTime)
          } else if (playerId) {
            await submitScore(playerId, category, finalScore, totalQuestions, finalTime, hintsUsed)
          }
          setScoreSubmitted(true)
        } catch (error) {
          console.error('Failed to submit score:', error)
        }
      }
    } else {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  if (showResults) {
    const percentage = Math.round((score / totalQuestions) * 100)
    const avgTimePerQuestion = totalQuestions > 0 ? Math.round(totalTimeTaken / totalQuestions) : 0
    let message = ''

    if (percentage === 100) {
      message = '🎉 Perfect Score! Amazing!'
    } else if (percentage >= 80) {
      message = '🌟 Excellent work!'
    } else if (percentage >= 60) {
      message = '👍 Good job!'
    } else if (percentage >= 40) {
      message = '📚 Keep practicing!'
    } else {
      message = '💪 Don\'t give up!'
    }

    return (
      <div className="quiz-results">
        <h2>Quiz Complete!</h2>
        <div className="result-message">{message}</div>
        <div className="score-display">
          <div className="score-number">{score}</div>
          <div className="score-label">out of {totalQuestions}</div>
        </div>
        <div className="score-percentage">
          {percentage}%
        </div>
        <div className="score-stats">
          <div className="stat-item">
            <span className="stat-label">⏱️ Total Time:</span>
            <span className="stat-value">{totalTimeTaken}s</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">⚡ Avg Time:</span>
            <span className="stat-value">{avgTimePerQuestion}s/question</span>
          </div>
          {hintsUsed > 0 && (
            <div className="stat-item">
              <span className="stat-label">💡 Hints Used:</span>
              <span className="stat-value">{hintsUsed}</span>
            </div>
          )}
        </div>
        {playerId && scoreSubmitted && (
          <div className="score-saved-message">
            ✓ Score saved to your profile
          </div>
        )}
        <button onClick={onRestart} className="restart-button">
          Play Again
        </button>
      </div>
    )
  }

  return (
    <div className="quiz-container">
      {showFeedback && (
        <AnswerFeedback
          isCorrect={isAnswerCorrect}
          correctAnswer={currentQuestion.correct_answer}
          onContinue={handleContinue}
        />
      )}

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
          <div className="mode-badge">📚 Solo Mode - Take Your Time</div>
        )}
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${((currentQuestionIndex + 1) / totalQuestions) * 100}%` }}
          />
        </div>
        <div className="question-counter">
          Question {currentQuestionIndex + 1} of {totalQuestions}
        </div>
      </div>

      <div className="hints-container">
        <button
          onClick={handleFiftyFifty}
          disabled={usedFiftyFifty[currentQuestionIndex] || (gameMode === 'timed' && timeExpired)}
          className="hint-button fifty-fifty"
          title="Eliminate 2 wrong answers"
        >
          50/50
        </button>
        <button
          onClick={handleSkip}
          disabled={skippedQuestions[currentQuestionIndex] || (gameMode === 'timed' && timeExpired)}
          className="hint-button skip"
          title="Skip this question"
        >
          ⏭️ Skip
        </button>
        <div className="hints-used">
          💡 Hints: {hintsUsed}
        </div>
      </div>

      {currentQuestion && (
        <Question
          question={currentQuestion}
          selectedAnswer={selectedAnswers[currentQuestionIndex]}
          onAnswerSelect={handleAnswerSelect}
          eliminatedChoices={eliminatedChoices[currentQuestionIndex] || []}
          disabled={gameMode === 'timed' && timeExpired}
        />
      )}

      <div className="quiz-navigation">
        {gameMode === 'solo' && (
          <button
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
            className="nav-button prev-button"
          >
            Previous
          </button>
        )}
        <button
          onClick={handleNext}
          className="nav-button next-button"
          disabled={gameMode === 'timed' && timeExpired}
        >
          {currentQuestionIndex === totalQuestions - 1 ? 'Finish' : 'Next'}
        </button>
      </div>
    </div>
  )
}

export default Quiz
