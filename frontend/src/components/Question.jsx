import './Question.css'

function Question({ question, selectedAnswer, onAnswerSelect, eliminatedChoices = [], disabled = false }) {
  return (
    <div className="question-container">
      <div className="question-text">{question.question}</div>
      <div className="choices-container">
        {question.choices.map((choice, index) => {
          const isEliminated = eliminatedChoices.includes(choice)
          return (
            <button
              key={index}
              onClick={() => !isEliminated && !disabled && onAnswerSelect(choice)}
              className={`choice-button ${
                selectedAnswer === choice ? 'selected' : ''
              } ${isEliminated ? 'eliminated' : ''} ${disabled ? 'disabled' : ''}`}
              disabled={isEliminated || disabled}
            >
              {isEliminated ? <span className="eliminated-mark">✕</span> : null}
              <span className={isEliminated ? 'eliminated-text' : ''}>{choice}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default Question