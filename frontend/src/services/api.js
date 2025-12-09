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

// Challenge Mode APIs
export const createChallenge = async (playerId, category, maxPlayers = 10) => {
  const response = await fetch(`${API_BASE_URL}/challenge/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      player_id: playerId,
      category,
      max_players: maxPlayers,
    }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to create challenge')
  }
  return response.json()
}

export const joinChallenge = async (playerId, roomCode) => {
  const response = await fetch(`${API_BASE_URL}/challenge/join`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      player_id: playerId,
      room_code: roomCode,
    }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to join challenge')
  }
  return response.json()
}

export const getChallenge = async (challengeId) => {
  const response = await fetch(`${API_BASE_URL}/challenge/${challengeId}`)
  if (!response.ok) throw new Error('Failed to fetch challenge')
  return response.json()
}

export const startChallenge = async (challengeId, playerId) => {
  const response = await fetch(`${API_BASE_URL}/challenge/${challengeId}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ player_id: playerId }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to start challenge')
  }
  return response.json()
}

export const submitChallengeScore = async (challengeId, playerId, score, totalQuestions, timeTaken) => {
  const response = await fetch(`${API_BASE_URL}/challenge/${challengeId}/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      player_id: playerId,
      score,
      total_questions: totalQuestions,
      time_taken: timeTaken,
    }),
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to submit challenge score')
  }
  return response.json()
}

export const getChallengeLeaderboard = async (challengeId) => {
  const response = await fetch(`${API_BASE_URL}/challenge/${challengeId}/leaderboard`)
  if (!response.ok) throw new Error('Failed to fetch challenge leaderboard')
  return response.json()
}

export const listChallenges = async (limit = 20) => {
  const response = await fetch(`${API_BASE_URL}/challenge/list?limit=${limit}`)
  if (!response.ok) throw new Error('Failed to fetch challenges')
  return response.json()
}

// Leaderboard reset APIs
export const resetLeaderboard = async () => {
  const response = await fetch(`${API_BASE_URL}/leaderboard/reset`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to reset leaderboard')
  }
  return response.json()
}

export const resetAllData = async () => {
  const response = await fetch(`${API_BASE_URL}/leaderboard/reset-all`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
  })
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.error || 'Failed to reset all data')
  }
  return response.json()
}