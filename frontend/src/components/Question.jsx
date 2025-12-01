import './Question.css'

function Question({ question, selectedAnswer, onAnswerSelect }) {
  return (
    <div className="question-container">
      <div className="question-text">{question.question}</div>
      <div className="choices-container">
        {question.choices.map((choice, index) => (
          <button
            key={index}
            onClick={() => onAnswerSelect(choice)}
            className={`choice-button ${
              selectedAnswer === choice ? 'selected' : ''
            }`}
          >
            {choice}
          </button>
        ))}
      </div>
    </div>
  )
}

export default Question

