import { useState, useEffect } from 'react'
import './Timer.css'

function Timer({ timeLimit, onTimeUp, isPaused = false }) {
  const [timeLeft, setTimeLeft] = useState(timeLimit)

  useEffect(() => {
    setTimeLeft(timeLimit)
  }, [timeLimit])

  useEffect(() => {
    if (isPaused || timeLeft <= 0) return

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(timer)
          onTimeUp()
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [timeLeft, isPaused, onTimeUp])

  const percentage = (timeLeft / timeLimit) * 100
  const isLow = percentage <= 25
  const isMedium = percentage <= 50 && percentage > 25

  return (
    <div className="timer-container">
      <div className="timer-display">
        <div className={`timer-circle ${isLow ? 'low' : isMedium ? 'medium' : ''}`}>
          <svg className="timer-svg" viewBox="0 0 100 100">
            <circle
              className="timer-bg"
              cx="50"
              cy="50"
              r="45"
            />
            <circle
              className="timer-progress"
              cx="50"
              cy="50"
              r="45"
              style={{
                strokeDasharray: `${percentage * 2.827}, 282.7`,
              }}
            />
          </svg>
          <div className="timer-text">
            <span className="timer-number">{timeLeft}</span>
            <span className="timer-label">sec</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Timer
