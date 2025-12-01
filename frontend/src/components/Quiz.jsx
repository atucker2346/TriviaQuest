import { useState } from 'react'
import Question from './Question'
import './Quiz.css'

function Quiz({ category, questions, onRestart }) {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [score, setScore] = useState(0)
  const [selectedAnswers, setSelectedAnswers] = useState({})
  const [showResults, setShowResults] = useState(false)

  const currentQuestion = questions[currentQuestionIndex]
  const totalQuestions = questions.length

  const handleAnswerSelect = (answer) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [currentQuestionIndex]: answer,
    })
  }

  const handleNext = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      // Calculate final score
      let finalScore = 0
      questions.forEach((q, index) => {
        if (selectedAnswers[index] === q.correct_answer) {
          finalScore++
        }
      })
      setScore(finalScore)
      setShowResults(true)
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  if (showResults) {
    return (
      <div className="quiz-results">
        <h2>Quiz Complete!</h2>
        <div className="score-display">
          <div className="score-number">{score}</div>
          <div className="score-label">out of {totalQuestions}</div>
        </div>
        <div className="score-percentage">
          {Math.round((score / totalQuestions) * 100)}%
        </div>
        <button onClick={onRestart} className="restart-button">
          Play Again
        </button>
      </div>
    )
  }

  return (
    <div className="quiz-container">
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

