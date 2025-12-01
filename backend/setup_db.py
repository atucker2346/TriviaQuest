import sqlite3
import json

# Connect or create database
conn = sqlite3.connect("questions.db")
cursor = conn.cursor()

# Create categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
""")

# Create questions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    choices TEXT NOT NULL,
    correct_answer TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")
