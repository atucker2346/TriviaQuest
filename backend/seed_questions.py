import sqlite3
import json

conn = sqlite3.connect("questions.db")
cursor = conn.cursor()

# Categories
categories = [
    "General Knowledge",
    "Science",
    "History",
    "Pop Culture",
    "Sports"
]

# Insert categories
for name in categories:
    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))

# Fetch category IDs
cursor.execute("SELECT id, name FROM categories")
category_map = {name: cid for cid, name in cursor.fetchall()}

# Sample questions (you can expand these later)
sample_questions = [
    {
        "category": "General Knowledge",
        "question": "What is the capital of France?",
        "choices": ["Paris", "Rome", "Berlin", "Madrid"],
        "correct": "Paris"
    },
    {
        "category": "Science",
        "question": "What planet is known as the Red Planet?",
        "choices": ["Venus", "Mars", "Jupiter", "Saturn"],
        "correct": "Mars"
    },
    {
        "category": "History",
        "question": "Who was the first President of the United States?",
        "choices": ["George Washington", "John Adams", "Thomas Jefferson", "James Monroe"],
        "correct": "George Washington"
    },
    {
        "category": "Pop Culture",
        "question": "Which singer is known as the 'Queen of Pop'?",
        "choices": ["Beyoncé", "Madonna", "Lady Gaga", "Ariana Grande"],
        "correct": "Madonna"
    },
    {
        "category": "Sports",
        "question": "How many players are on a standard soccer team on the field?",
        "choices": ["9", "10", "11", "12"],
        "correct": "11"
    }
]

# Insert sample questions
for q in sample_questions:
    cursor.execute("""
        INSERT INTO questions (category_id, question, choices, correct_answer)
        VALUES (?, ?, ?, ?)
    """, (
        category_map[q["category"]],
        q["question"],
        json.dumps(q["choices"]),   # store as JSON string
        q["correct"]
    ))

conn.commit()
conn.close()

print("Sample questions added!")
