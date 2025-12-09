import './CategorySelection.css'

function CategorySelection({ categories, onSelect, loading, onBack }) {
  return (
    <div className="category-selection">
      <div className="category-header">
        <button onClick={onBack} className="back-button" title="Go back">
          ← Back
        </button>
        <h2>Select a Category</h2>
      </div>
      <div className="categories-grid">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => onSelect(category)}
            disabled={loading}
            className="category-button"
          >
            {category}
          </button>
        ))}
      </div>
      {loading && <div className="loading-text">Loading questions...</div>}
    </div>
  )
}

export default CategorySelection

