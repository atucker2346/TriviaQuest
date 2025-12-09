import './AnswerFeedback.css'

function AnswerFeedback({ isCorrect, correctAnswer, onContinue }) {
  return (
    <div className={`feedback-overlay ${isCorrect ? 'correct' : 'incorrect'}`}>
      <div className="feedback-container">
        <div className="feedback-icon">
          {isCorrect ? (
            <svg viewBox="0 0 100 100" className="checkmark">
              <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="4"/>
              <path d="M30 50 L45 65 L70 35" fill="none" stroke="currentColor" strokeWidth="6" strokeLinecap="round"/>
            </svg>
          ) : (
            <svg viewBox="0 0 100 100" className="cross">
              <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="4"/>
              <path d="M35 35 L65 65 M65 35 L35 65" stroke="currentColor" strokeWidth="6" strokeLinecap="round"/>
            </svg>
          )}
        </div>
        <h2 className="feedback-title">
          {isCorrect ? "You're Correct!" : "Wrong Answer"}
        </h2>
        {!isCorrect && (
          <p className="correct-answer-text">
            The correct answer is: <strong>{correctAnswer}</strong>
          </p>
        )}
        <button onClick={onContinue} className="continue-button">
          Continue
        </button>
      </div>
    </div>
  )
}

export default AnswerFeedback

