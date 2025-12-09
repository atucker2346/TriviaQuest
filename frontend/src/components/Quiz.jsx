import { useState } from 'react'
import Question from './Question'
import AnswerFeedback from './AnswerFeedback'
import { submitScore } from '../services/api'
import './Quiz.css'

function Quiz({ category, questions, onRestart, playerId }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [showResults, setShowResults] = useState(false)
  const [showFeedback, setShowFeedback] = useState(false)
  const [isAnswerCorrect, setIsAnswerCorrect] = useState(false)
  const [scoreSubmitted, setScoreSubmitted] = useState(false)

  const currentQuestion = questions[currentQuestionIndex]
  const totalQuestions = questions.length

  const handleAnswerSelect = (answer) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [currentQuestionIndex]: answer,
    })
  }

  const handleNext = () => {
    const selectedAnswer = selectedAnswers[currentQuestionIndex]

    if (!selectedAnswer) {
      alert('Please select an answer before continuing')
      return
    }

    const isCorrect = selectedAnswer === currentQuestion.correct_answer
    setIsAnswerCorrect(isCorrect)

    if (isCorrect) {
      setScore(score + 1)
    }

    setShowFeedback(true)
  }

  const calculateScore = () => {
    let total = 0
    questions.forEach((q, index) => {
      if (selectedAnswers[index] === q.correct_answer) {
        total++
      }
    })
    return total
  }

  const handleContinue = async () => {
    setShowFeedback(false)

    const isLastQuestion = currentQuestionIndex >= totalQuestions - 1

    if (isLastQuestion) {
      const finalScore = calculateScore()
      setScore(finalScore)
      setShowResults(true)

      if (playerId && !scoreSubmitted) {
        try {
          await submitScore(playerId, category, finalScore, totalQuestions)
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

      {currentQuestion && (
        <Question
          question={currentQuestion}
          selectedAnswer={selectedAnswers[currentQuestionIndex]}
          onAnswerSelect={handleAnswerSelect}
        />
      )}

      <div className="quiz-navigation">
        <button
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
          className="nav-button prev-button"
        >
          Previous
        </button>
        <button
          onClick={handleNext}
          className="nav-button next-button"
        >
          {currentQuestionIndex === totalQuestions - 1 ? 'Finish' : 'Next'}
        </button>
      </div>
    </div>
  )
}

export default Quiz

