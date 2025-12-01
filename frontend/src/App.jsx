import { useState, useEffect } from 'react'
import { fetchCategories, fetchQuestions } from './services/api'
import CategorySelection from './components/CategorySelection'
import Quiz from './components/Quiz'
import './App.css'

function App() {
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadCategories()
  }, [])

  const loadCategories = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchCategories()
      setCategories(data)
    } catch (err) {
      setError('Failed to load categories. Make sure the backend is running.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCategorySelect = async (category) => {
    try {
      setLoading(true)
      setError(null)
      const data = await fetchQuestions(category)
      setQuestions(data)
      setSelectedCategory(category)
    } catch (err) {
      setError('Failed to load questions. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleRestart = () => {
    setSelectedCategory(null)
    setQuestions([])
  }

  if (loading && !selectedCategory) {
    return (
      <div className="app-container">
        <div className="loading">Loading categories...</div>
      </div>
    )
  }

  if (error && !selectedCategory) {
    return (
      <div className="app-container">
        <div className="error">{error}</div>
        <button onClick={loadCategories} className="retry-button">
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="app-container">
      <h1 className="app-title">TriviaQuest</h1>
      {!selectedCategory ? (
        <CategorySelection
          categories={categories}
          onSelect={handleCategorySelect}
          loading={loading}
        />
      ) : (
        <Quiz
          category={selectedCategory}
          questions={questions}
          onRestart={handleRestart}
        />
      )}
    </div>
  )
}

export default App

