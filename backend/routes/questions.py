from flask import Blueprint, jsonify
import sqlite3
import json
import random

questions_bp = Blueprint("questions", __name__)

def get_db():
    conn = sqlite3.connect("questions.db")
    conn.row_factory = sqlite3.Row
    return conn

@questions_bp.route("/categories")
def get_categories():
    conn = get_db()
    rows = conn.execute("SELECT name FROM categories").fetchall()
    conn.close()
    return jsonify([row["name"] for row in rows])

@questions_bp.route("/questions/<category>")
def get_questions(category):
    conn = get_db()

    # Get category ID
    row = conn.execute(
        "SELECT id FROM categories WHERE name = ?", (category,)
    ).fetchone()

    if not row:
        return jsonify({"error": "Category not found"}), 404
    
    category_id = row["id"]

    # Fetch all questions for the category
    rows = conn.execute(
        "SELECT * FROM questions WHERE category_id = ?", (category_id,)
    ).fetchall()
    conn.close()

    # Pick 10 random ones (or fewer if database is small)
    selected = random.sample(rows, min(10, len(rows)))

    # Convert DB rows to dicts
    questions = []
    for q in selected:
        questions.append({
            "id": q["id"],
            "question": q["question"],
            "choices": json.loads(q["choices"]),
            "correct_answer": q["correct_answer"]
        })

    return jsonify(questions)
