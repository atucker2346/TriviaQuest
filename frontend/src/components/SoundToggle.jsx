import { useState } from 'react'
import { soundManager } from '../utils/sounds'
import './SoundToggle.css'

function SoundToggle() {
  const [isEnabled, setIsEnabled] = useState(soundManager.isEnabled())

  const toggleSound = () => {
    const newState = soundManager.toggle()
    setIsEnabled(newState)
  }

  return (
    <button 
      className="sound-toggle" 
      onClick={toggleSound}
      aria-label="Toggle sound"
      title={isEnabled ? 'Mute sounds' : 'Enable sounds'}
    >
      {isEnabled ? '🔊' : '🔇'}
    </button>
  )
}

export default SoundToggle
