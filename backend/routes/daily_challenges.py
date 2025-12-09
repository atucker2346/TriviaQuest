from flask import Blueprint, jsonify, request
import sqlite3
import json
import random
import os
from datetime import date, datetime, timedelta

daily_challenges_bp = Blueprint("daily_challenges", __name__)

def get_db():
    """Get database connection"""
    db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(db_dir, "questions.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@daily_challenges_bp.route("/daily-challenge/today")
def get_today_challenge():
    """Get or create today's daily challenge"""
    try:
        today = date.today().isoformat()
        conn = get_db()
        
        # Check if today's challenge exists
        challenge = conn.execute(
            "SELECT * FROM daily_challenges WHERE date = ?",
            (today,)
        ).fetchone()
        
        if not challenge:
            # Create today's challenge
            # Pick a random category
            categories = conn.execute("SELECT name FROM categories").fetchall()
            if not categories:
                conn.close()
                return jsonify({"error": "No categories available"}), 404
            
            category = random.choice(categories)["name"]
            
            # Get category ID
            category_row = conn.execute(
                "SELECT id FROM categories WHERE name = ?",
                (category,)
            ).fetchone()
            category_id = category_row["id"]
            
            # Get 10 random questions from this category
            questions = conn.execute(
                "SELECT id FROM questions WHERE category_id = ? ORDER BY RANDOM() LIMIT 10",
                (category_id,)
            ).fetchall()
            
            if len(questions) < 10:
                conn.close()
                return jsonify({"error": "Not enough questions for daily challenge"}), 500
            
            question_ids = json.dumps([q["id"] for q in questions])
            
            # Insert new challenge
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO daily_challenges (date, category, question_ids)
                VALUES (?, ?, ?)
                """,
                (today, category, question_ids)
            )
            conn.commit()
            challenge_id = cursor.lastrowid
            
            # Fetch the newly created challenge
            challenge = conn.execute(
                "SELECT * FROM daily_challenges WHERE id = ?",
                (challenge_id,)
            ).fetchone()
        
        # Get the questions for this challenge
        question_ids = json.loads(challenge["question_ids"])
        questions = []
        
        for qid in question_ids:
            q = conn.execute(
                "SELECT * FROM questions WHERE id = ?",
                (qid,)
            ).fetchone()
            if q:
                questions.append({
                    "id": q["id"],
                    "question": q["question"],
                    "choices": json.loads(q["choices"]),
                    "correct_answer": q["correct_answer"],
                    "time_limit": q["time_limit"]
                })
        
        conn.close()
        
        return jsonify({
            "challenge_id": challenge["id"],
            "date": challenge["date"],
            "category": challenge["category"],
            "questions": questions
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch daily challenge", "details": str(e)}), 500

@daily_challenges_bp.route("/daily-challenge/submit", methods=["POST"])
def submit_daily_challenge():
    """Submit daily challenge score"""
    try:
        data = request.get_json()
        challenge_id = data.get("challenge_id")
        player_id = data.get("player_id")
        score = data.get("score")
        total_questions = data.get("total_questions")
        time_taken = data.get("time_taken", 0)
        
        if not all([challenge_id, player_id, score is not None, total_questions]):
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if player already completed today's challenge
        existing = conn.execute(
            """
            SELECT id FROM daily_challenge_scores 
            WHERE challenge_id = ? AND player_id = ?
            """,
            (challenge_id, player_id)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({"error": "Challenge already completed today"}), 400
        
        # Insert score
        cursor.execute(
            """
            INSERT INTO daily_challenge_scores 
            (challenge_id, player_id, score, total_questions, time_taken)
            VALUES (?, ?, ?, ?, ?)
            """,
            (challenge_id, player_id, score, total_questions, time_taken)
        )
        
        # Update streak
        update_player_streak(conn, player_id)
        
        conn.commit()
        
        # Get updated streak info
        streak = conn.execute(
            "SELECT * FROM player_streaks WHERE player_id = ?",
            (player_id,)
        ).fetchone()
        
        conn.close()
        
        return jsonify({
            "message": "Daily challenge completed!",
            "current_streak": streak["current_streak"] if streak else 0,
            "longest_streak": streak["longest_streak"] if streak else 0
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to submit daily challenge", "details": str(e)}), 500

def update_player_streak(conn, player_id):
    """Update player's streak information"""
    cursor = conn.cursor()
    today = date.today()
    
    # Get current streak info
    streak = conn.execute(
        "SELECT * FROM player_streaks WHERE player_id = ?",
        (player_id,)
    ).fetchone()
    
    if not streak:
        # First time playing daily challenge
        cursor.execute(
            """
            INSERT INTO player_streaks (player_id, current_streak, longest_streak, last_played_date)
            VALUES (?, 1, 1, ?)
            """,
            (player_id, today.isoformat())
        )
    else:
        last_played = date.fromisoformat(streak["last_played_date"])
        days_diff = (today - last_played).days
        
        if days_diff == 0:
            # Already played today (shouldn't happen due to unique constraint)
            pass
        elif days_diff == 1:
            # Consecutive day - increment streak
            new_streak = streak["current_streak"] + 1
            new_longest = max(new_streak, streak["longest_streak"])
            cursor.execute(
                """
                UPDATE player_streaks 
                SET current_streak = ?, longest_streak = ?, last_played_date = ?
                WHERE player_id = ?
                """,
                (new_streak, new_longest, today.isoformat(), player_id)
            )
        else:
            # Streak broken - reset to 1
            cursor.execute(
                """
                UPDATE player_streaks 
                SET current_streak = 1, last_played_date = ?
                WHERE player_id = ?
                """,
                (today.isoformat(), player_id)
            )

@daily_challenges_bp.route("/daily-challenge/leaderboard")
def get_daily_leaderboard():
    """Get leaderboard for today's daily challenge"""
    try:
        today = date.today().isoformat()
        limit = request.args.get("limit", 100, type=int)
        
        conn = get_db()
        
        # Get today's challenge
        challenge = conn.execute(
            "SELECT id FROM daily_challenges WHERE date = ?",
            (today,)
        ).fetchone()
        
        if not challenge:
            conn.close()
            return jsonify([])
        
        # Get leaderboard
        rows = conn.execute(
            """
            SELECT 
                p.id,
                p.username,
                dcs.score,
                dcs.total_questions,
                dcs.time_taken,
                dcs.completed_at
            FROM daily_challenge_scores dcs
            JOIN players p ON dcs.player_id = p.id
            WHERE dcs.challenge_id = ?
            ORDER BY dcs.score DESC, dcs.time_taken ASC
            LIMIT ?
            """,
            (challenge["id"], limit)
        ).fetchall()
        
        conn.close()
        
        leaderboard = []
        for idx, row in enumerate(rows, 1):
            leaderboard.append({
                "rank": idx,
                "player_id": row["id"],
                "username": row["username"],
                "score": row["score"],
                "total_questions": row["total_questions"],
                "percentage": round((row["score"] / row["total_questions"]) * 100, 2),
                "time_taken": row["time_taken"],
                "completed_at": row["completed_at"]
            })
        
        return jsonify(leaderboard)
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch daily leaderboard", "details": str(e)}), 500

@daily_challenges_bp.route("/player/<int:player_id>/streak")
def get_player_streak(player_id):
    """Get player's streak information"""
    try:
        conn = get_db()
        
        streak = conn.execute(
            "SELECT * FROM player_streaks WHERE player_id = ?",
            (player_id,)
        ).fetchone()
        
        # Check if player completed today's challenge
        today = date.today().isoformat()
        challenge = conn.execute(
            "SELECT id FROM daily_challenges WHERE date = ?",
            (today,)
        ).fetchone()
        
        completed_today = False
        if challenge:
            completed = conn.execute(
                """
                SELECT id FROM daily_challenge_scores 
                WHERE challenge_id = ? AND player_id = ?
                """,
                (challenge["id"], player_id)
            ).fetchone()
            completed_today = completed is not None
        
        conn.close()
        
        if not streak:
            return jsonify({
                "current_streak": 0,
                "longest_streak": 0,
                "last_played_date": None,
                "completed_today": completed_today
            })
        
        return jsonify({
            "current_streak": streak["current_streak"],
            "longest_streak": streak["longest_streak"],
            "last_played_date": streak["last_played_date"],
            "completed_today": completed_today
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch streak", "details": str(e)}), 500
