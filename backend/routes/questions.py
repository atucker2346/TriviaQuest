from flask import Blueprint, jsonify
import sqlite3
import json
import random
import os

questions_bp = Blueprint("questions", __name__)

def get_db():
    # Get the directory where this file is located
    db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(db_dir, "questions.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@questions_bp.route("/categories")
def get_categories():
    try:
        conn = get_db()
        rows = conn.execute("SELECT name FROM categories").fetchall()
        conn.close()
        return jsonify([row["name"] for row in rows])
    except Exception as e:
        return jsonify({"error": "Failed to fetch categories", "details": str(e)}), 500

@questions_bp.route("/questions/<category>")
def get_questions(category):
    try:
        conn = get_db()

        # Get category ID
        row = conn.execute(
            "SELECT id FROM categories WHERE name = ?", (category,)
        ).fetchone()

        if not row:
            conn.close()
            return jsonify({"error": "Category not found"}), 404
        
        category_id = row["id"]

        # Fetch all questions for the category
        rows = conn.execute(
            "SELECT * FROM questions WHERE category_id = ?", (category_id,)
        ).fetchall()
        conn.close()

        if not rows:
            return jsonify({"error": "No questions found for this category"}), 404

        # Pick 10 random ones (or fewer if database is small)
        # Handle case where there are fewer questions than requested
        num_questions = min(10, len(rows))
        selected = random.sample(rows, num_questions)

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
    except ValueError as e:
        # Handle random.sample error if it occurs
        return jsonify({"error": "Failed to select questions", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to fetch questions", "details": str(e)}), 500
