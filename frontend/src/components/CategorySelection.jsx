import './CategorySelection.css'

function CategorySelection({ categories, onSelect, loading }) {
  return (
    <div className="category-selection">
      <h2>Select a Category</h2>
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

