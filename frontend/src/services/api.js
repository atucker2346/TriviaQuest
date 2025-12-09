const API_BASE_URL = 'http://localhost:5001'

export const fetchCategories = async ( ) => {
  const response = await fetch(`${API_BASE_URL}/categories`)
  if (!response.ok) {
    throw new Error('Failed to fetch categories')
  }
  return response.json()
}

export const fetchQuestions = async (category) => {
  const response = await fetch(`${API_BASE_URL}/questions/${encodeURIComponent(category)}`)
  if (!response.ok) {
    throw new Error('Failed to fetch questions')
  }
  return response.json()
}

export const registerPlayer = async (username) => {
  const response = await fetch(`${API_BASE_URL}/player/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to register player')
  }
  return response.json()
}

export const submitScore = async (playerId, category, score, totalQuestions, timeTaken = 0, hintsUsed = 0) => {
  const response = await fetch(`${API_BASE_URL}/score/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      player_id: playerId,
      category,
      score,
      total_questions: totalQuestions,
      time_taken: timeTaken,
      hints_used: hintsUsed,
    }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to submit score')
  }
  return response.json()
}

export const fetchPlayerStats = async (playerId) => {
  const response = await fetch(`${API_BASE_URL}/player/${playerId}/stats`)
  if (!response.ok) {
    throw new Error('Failed to fetch player stats')
  }
  return response.json()
}

export const fetchGlobalLeaderboard = async (limit = 100) => {
  const response = await fetch(`${API_BASE_URL}/leaderboard/global?limit=${limit}`)
  if (!response.ok) {
    throw new Error('Failed to fetch leaderboard')
  }
  return response.json()
}

// Daily Challenge APIs
export const getTodayChallenge = async () => {
  const response = await fetch(`${API_BASE_URL}/daily-challenge/today`)
  if (!response.ok) throw new Error('Failed to fetch daily challenge')
  return response.json()
}

export const submitDailyChallenge = async (challengeId, playerId, score, totalQuestions, timeTaken) => {
  const response = await fetch(`${API_BASE_URL}/daily-challenge/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      challenge_id: challengeId,
      player_id: playerId,
      score,
      total_questions: totalQuestions,
      time_taken: timeTaken,
    }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to submit daily challenge')
  }
  return response.json()
}

export const getDailyLeaderboard = async (limit = 100) => {
  const response = await fetch(`${API_BASE_URL}/daily-challenge/leaderboard?limit=${limit}`)
  if (!response.ok) throw new Error('Failed to fetch daily leaderboard')
  return response.json()
}

export const getPlayerStreak = async (playerId) => {
  const response = await fetch(`${API_BASE_URL}/player/${playerId}/streak`)
  if (!response.ok) throw new Error('Failed to fetch player streak')
  return response.json()
}
