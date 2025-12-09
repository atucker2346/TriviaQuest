const API_BASE_URL = 'http://localhost:5001'

export const fetchCategories = async () => {
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

export const submitScore = async (playerId, category, score, totalQuestions) => {
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

