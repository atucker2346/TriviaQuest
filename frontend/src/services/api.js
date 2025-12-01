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

