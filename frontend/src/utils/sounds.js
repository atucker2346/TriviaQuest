// Sound effects utility
const SOUND_BASE_URL = 'http://localhost:5001/static/sounds'

class SoundManager {
  constructor( ) {
    this.sounds = {
      correct: new Audio(`${SOUND_BASE_URL}/correct.mp3`),
      wrong: new Audio(`${SOUND_BASE_URL}/wrong.mp3`),
    }
    
    // Preload sounds
    Object.values(this.sounds).forEach(sound => {
      sound.load()
    })
    
    // Check if sound is enabled
    this.enabled = localStorage.getItem('soundEnabled') !== 'false'
  }

  play(soundName) {
    if (!this.enabled || !this.sounds[soundName]) return
    
    const sound = this.sounds[soundName]
    sound.currentTime = 0
    sound.play().catch(err => {
      console.warn('Failed to play sound:', err)
    })
  }

  playCorrect() {
    this.play('correct')
  }

  playWrong() {
    this.play('wrong')
  }

  toggle() {
    this.enabled = !this.enabled
    localStorage.setItem('soundEnabled', this.enabled)
    return this.enabled
  }

  isEnabled() {
    return this.enabled
  }
}

export const soundManager = new SoundManager()
