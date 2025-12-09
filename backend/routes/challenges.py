from flask import Blueprint, jsonify, request
import sqlite3
import json
import random
import os
import string
from datetime import datetime, timedelta

challenges_bp = Blueprint("challenges", __name__)

def get_db():
    """Get database connection"""
    db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(db_dir, "questions.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def generate_room_code():
    """Generate a unique 6-character room code"""
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        conn = get_db()
        existing = conn.execute(
            "SELECT id FROM challenge_rooms WHERE room_code = ?",
            (code,)
        ).fetchone()
        conn.close()
        if not existing:
            return code

@challenges_bp.route("/challenge/create", methods=["POST"])
def create_challenge():
    """Create a new challenge room"""
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        category = data.get("category")
        max_players = data.get("max_players", 10)
        
        if not player_id or not category:
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db()
        
        # Get questions for the category
        category_row = conn.execute(
            "SELECT id FROM categories WHERE name = ?",
            (category,)
        ).fetchone()
        
        if not category_row:
            conn.close()
            return jsonify({"error": "Category not found"}), 404
        
        category_id = category_row["id"]
        questions = conn.execute(
            "SELECT id FROM questions WHERE category_id = ? ORDER BY RANDOM() LIMIT 10",
            (category_id,)
        ).fetchall()
        
        if len(questions) < 10:
            conn.close()
            return jsonify({"error": "Not enough questions for this category"}), 400
        
        question_ids = json.dumps([q["id"] for q in questions])
        room_code = generate_room_code()
        
        # Create challenge room (expires in 1 hour)
        expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO challenge_rooms (room_code, category, question_ids, created_by, max_players, expires_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (room_code, category, question_ids, player_id, max_players, expires_at)
        )
        challenge_id = cursor.lastrowid
        
        # Add creator as participant
        cursor.execute(
            """
            INSERT INTO challenge_participants (challenge_id, player_id, status)
            VALUES (?, ?, 'waiting')
            """,
            (challenge_id, player_id)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "challenge_id": challenge_id,
            "room_code": room_code,
            "category": category,
            "max_players": max_players
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to create challenge", "details": str(e)}), 500

@challenges_bp.route("/challenge/join", methods=["POST"])
def join_challenge():
    """Join a challenge room by room code"""
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        room_code = data.get("room_code", "").upper().strip()
        
        if not player_id or not room_code:
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db()
        
        # Find challenge room
        challenge = conn.execute(
            "SELECT * FROM challenge_rooms WHERE room_code = ?",
            (room_code,)
        ).fetchone()
        
        if not challenge:
            conn.close()
            return jsonify({"error": "Challenge room not found"}), 404
        
        # Check if expired
        if challenge["expires_at"]:
            expires_at = datetime.fromisoformat(challenge["expires_at"])
            if datetime.now() > expires_at:
                conn.close()
                return jsonify({"error": "Challenge room has expired"}), 400
        
        # Check if already joined
        existing = conn.execute(
            "SELECT id FROM challenge_participants WHERE challenge_id = ? AND player_id = ?",
            (challenge["id"], player_id)
        ).fetchone()
        
        if existing:
            conn.close()
            return jsonify({"error": "Already joined this challenge"}), 400
        
        # Check if room is full
        participant_count = conn.execute(
            "SELECT COUNT(*) as count FROM challenge_participants WHERE challenge_id = ?",
            (challenge["id"],)
        ).fetchone()["count"]
        
        if participant_count >= challenge["max_players"]:
            conn.close()
            return jsonify({"error": "Challenge room is full"}), 400
        
        # Check if challenge has started
        if challenge["status"] == "active":
            conn.close()
            return jsonify({"error": "Challenge has already started"}), 400
        
        # Add participant
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO challenge_participants (challenge_id, player_id, status)
            VALUES (?, ?, 'waiting')
            """,
            (challenge["id"], player_id)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "challenge_id": challenge["id"],
            "room_code": challenge["room_code"],
            "category": challenge["category"]
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to join challenge", "details": str(e)}), 500

@challenges_bp.route("/challenge/<int:challenge_id>")
def get_challenge(challenge_id):
    """Get challenge details and questions"""
    try:
        conn = get_db()
        
        challenge = conn.execute(
            "SELECT * FROM challenge_rooms WHERE id = ?",
            (challenge_id,)
        ).fetchone()
        
        if not challenge:
            conn.close()
            return jsonify({"error": "Challenge not found"}), 404
        
        # Get participants
        participants = conn.execute(
            """
            SELECT p.id, p.username, cp.status, cp.score, cp.total_questions, cp.time_taken
            FROM challenge_participants cp
            JOIN players p ON cp.player_id = p.id
            WHERE cp.challenge_id = ?
            ORDER BY cp.joined_at
            """,
            (challenge_id,)
        ).fetchall()
        
        # Get questions
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
                    "time_limit": q.get("time_limit", 60)
                })
        
        conn.close()
        
        return jsonify({
            "challenge_id": challenge["id"],
            "room_code": challenge["room_code"],
            "category": challenge["category"],
            "status": challenge["status"],
            "max_players": challenge["max_players"],
            "created_at": challenge["created_at"],
            "participants": [dict(p) for p in participants],
            "questions": questions
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch challenge", "details": str(e)}), 500

@challenges_bp.route("/challenge/<int:challenge_id>/start", methods=["POST"])
def start_challenge(challenge_id):
    """Start a challenge (only creator can start)"""
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        
        if not player_id:
            return jsonify({"error": "Missing player_id"}), 400
        
        conn = get_db()
        
        challenge = conn.execute(
            "SELECT * FROM challenge_rooms WHERE id = ?",
            (challenge_id,)
        ).fetchone()
        
        if not challenge:
            conn.close()
            return jsonify({"error": "Challenge not found"}), 404
        
        if challenge["created_by"] != player_id:
            conn.close()
            return jsonify({"error": "Only the creator can start the challenge"}), 403
        
        if challenge["status"] != "waiting":
            conn.close()
            return jsonify({"error": "Challenge has already started or completed"}), 400
        
        # Update challenge status
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE challenge_rooms 
            SET status = 'active', started_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (challenge_id,)
        )
        
        # Update all participants to 'playing'
        cursor.execute(
            """
            UPDATE challenge_participants 
            SET status = 'playing', started_at = CURRENT_TIMESTAMP
            WHERE challenge_id = ?
            """,
            (challenge_id,)
        )
        
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Challenge started"})
        
    except Exception as e:
        return jsonify({"error": "Failed to start challenge", "details": str(e)}), 500

@challenges_bp.route("/challenge/<int:challenge_id>/submit", methods=["POST"])
def submit_challenge_score(challenge_id):
    """Submit score for a challenge"""
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        score = data.get("score")
        total_questions = data.get("total_questions")
        time_taken = data.get("time_taken", 0)
        
        if not all([player_id, score is not None, total_questions]):
            return jsonify({"error": "Missing required fields"}), 400
        
        conn = get_db()
        
        # Check if challenge exists and is active
        challenge = conn.execute(
            "SELECT * FROM challenge_rooms WHERE id = ?",
            (challenge_id,)
        ).fetchone()
        
        if not challenge:
            conn.close()
            return jsonify({"error": "Challenge not found"}), 404
        
        if challenge["status"] != "active":
            conn.close()
            return jsonify({"error": "Challenge is not active"}), 400
        
        # Update participant score
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE challenge_participants 
            SET status = 'completed', 
                score = ?, 
                total_questions = ?, 
                time_taken = ?,
                completed_at = CURRENT_TIMESTAMP
            WHERE challenge_id = ? AND player_id = ?
            """,
            (score, total_questions, time_taken, challenge_id, player_id)
        )
        
        # Check if all participants have completed
        remaining = conn.execute(
            """
            SELECT COUNT(*) as count 
            FROM challenge_participants 
            WHERE challenge_id = ? AND status != 'completed'
            """,
            (challenge_id,)
        ).fetchone()["count"]
        
        if remaining == 0:
            # All participants completed, mark challenge as completed
            cursor.execute(
                "UPDATE challenge_rooms SET status = 'completed' WHERE id = ?",
                (challenge_id,)
            )
        
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Score submitted successfully"})
        
    except Exception as e:
        return jsonify({"error": "Failed to submit score", "details": str(e)}), 500

@challenges_bp.route("/challenge/<int:challenge_id>/leaderboard")
def get_challenge_leaderboard(challenge_id):
    """Get real-time leaderboard for a challenge"""
    try:
        conn = get_db()
        
        participants = conn.execute(
            """
            SELECT 
                p.id,
                p.username,
                cp.score,
                cp.total_questions,
                cp.time_taken,
                cp.status,
                cp.completed_at,
                CASE 
                    WHEN cp.total_questions > 0 THEN ROUND((cp.score * 100.0 / cp.total_questions), 2)
                    ELSE 0
                END as percentage
            FROM challenge_participants cp
            JOIN players p ON cp.player_id = p.id
            WHERE cp.challenge_id = ?
            ORDER BY 
                cp.score DESC,
                cp.time_taken ASC,
                cp.completed_at ASC
            """,
            (challenge_id,)
        ).fetchall()
        
        conn.close()
        
        leaderboard = []
        for idx, p in enumerate(participants, 1):
            leaderboard.append({
                "rank": idx,
                "player_id": p["id"],
                "username": p["username"],
                "score": p["score"],
                "total_questions": p["total_questions"],
                "percentage": p["percentage"],
                "time_taken": p["time_taken"],
                "status": p["status"],
                "completed_at": p["completed_at"]
            })
        
        return jsonify(leaderboard)
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch leaderboard", "details": str(e)}), 500

@challenges_bp.route("/challenge/list")
def list_challenges():
    """List available public challenges"""
    try:
        limit = request.args.get("limit", 20, type=int)
        
        conn = get_db()
        
        challenges = conn.execute(
            """
            SELECT 
                cr.id,
                cr.room_code,
                cr.category,
                cr.status,
                cr.max_players,
                cr.created_at,
                COUNT(cp.id) as participant_count,
                p.username as creator_name
            FROM challenge_rooms cr
            LEFT JOIN challenge_participants cp ON cr.id = cp.challenge_id
            JOIN players p ON cr.created_by = p.id
            WHERE cr.status = 'waiting' AND cr.expires_at > datetime('now')
            GROUP BY cr.id
            HAVING participant_count < cr.max_players
            ORDER BY cr.created_at DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()
        
        conn.close()
        
        return jsonify([dict(c) for c in challenges])
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch challenges", "details": str(e)}), 500

