from flask import Blueprint, jsonify, request
import sqlite3
import os

scoreboard_bp = Blueprint("scoreboard", __name__)

def get_db():
    """Get database connection"""
    db_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(db_dir, "questions.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@scoreboard_bp.route("/player/register", methods=["POST"])
def register_player():
    """Register a new player or get existing player ID"""
    try:
        data = request.get_json()
        username = data.get("username", "").strip()
        
        if not username:
            return jsonify({"error": "Username is required"}), 400
        
        if len(username) < 3 or len(username) > 20:
            return jsonify({"error": "Username must be between 3 and 20 characters"}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Try to insert new player
        try:
            cursor.execute(
                "INSERT INTO players (username) VALUES (?)",
                (username,)
            )
            conn.commit()
            player_id = cursor.lastrowid
            conn.close()
            return jsonify({
                "player_id": player_id,
                "username": username,
                "is_new": True
            })
        except sqlite3.IntegrityError:
            # Player already exists, get their ID
            row = cursor.execute(
                "SELECT id FROM players WHERE username = ?",
                (username,)
            ).fetchone()
            conn.close()
            return jsonify({
                "player_id": row["id"],
                "username": username,
                "is_new": False
            })
            
    except Exception as e:
        return jsonify({"error": "Failed to register player", "details": str(e)}), 500

@scoreboard_bp.route("/score/submit", methods=["POST"])
def submit_score():
    """Submit a quiz score"""
    try:
        data = request.get_json()
        player_id = data.get("player_id")
        category = data.get("category")
        score = data.get("score")
        total_questions = data.get("total_questions")
        
        if not all([player_id, category, score is not None, total_questions]):
            return jsonify({"error": "Missing required fields"}), 400
        
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO scores (player_id, category, score, total_questions, percentage)
            VALUES (?, ?, ?, ?, ?)
            """,
            (player_id, category, score, total_questions, percentage)
        )
        
        conn.commit()
        score_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "score_id": score_id,
            "message": "Score submitted successfully"
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to submit score", "details": str(e)}), 500

@scoreboard_bp.route("/player/<int:player_id>/stats")
def get_player_stats(player_id):
    """Get player statistics"""
    try:
        conn = get_db()
        
        # Get player info
        player = conn.execute(
            "SELECT * FROM players WHERE id = ?",
            (player_id,)
        ).fetchone()
        
        if not player:
            conn.close()
            return jsonify({"error": "Player not found"}), 404
        
        # Get total games played
        total_games = conn.execute(
            "SELECT COUNT(*) as count FROM scores WHERE player_id = ?",
            (player_id,)
        ).fetchone()["count"]
        
        # Get total score
        total_score = conn.execute(
            "SELECT SUM(score) as total FROM scores WHERE player_id = ?",
            (player_id,)
        ).fetchone()["total"] or 0
        
        # Get total questions
        total_questions = conn.execute(
            "SELECT SUM(total_questions) as total FROM scores WHERE player_id = ?",
            (player_id,)
        ).fetchone()["total"] or 0
        
        # Get average percentage
        avg_percentage = conn.execute(
            "SELECT AVG(percentage) as avg FROM scores WHERE player_id = ?",
            (player_id,)
        ).fetchone()["avg"] or 0
        
        # Get best score
        best_score = conn.execute(
            """
            SELECT category, score, total_questions, percentage, played_at
            FROM scores
            WHERE player_id = ?
            ORDER BY percentage DESC, score DESC
            LIMIT 1
            """,
            (player_id,)
        ).fetchone()
        
        # Get recent scores
        recent_scores = conn.execute(
            """
            SELECT category, score, total_questions, percentage, played_at
            FROM scores
            WHERE player_id = ?
            ORDER BY played_at DESC
            LIMIT 10
            """,
            (player_id,)
        ).fetchall()
        
        conn.close()
        
        return jsonify({
            "player": {
                "id": player["id"],
                "username": player["username"],
                "created_at": player["created_at"]
            },
            "stats": {
                "total_games": total_games,
                "total_score": total_score,
                "total_questions": total_questions,
                "average_percentage": round(avg_percentage, 2)
            },
            "best_score": dict(best_score) if best_score else None,
            "recent_scores": [dict(row) for row in recent_scores]
        })
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch player stats", "details": str(e)}), 500

@scoreboard_bp.route("/leaderboard/global")
def get_global_leaderboard():
    """Get global leaderboard"""
    try:
        limit = request.args.get("limit", 100, type=int)
        
        conn = get_db()
        
        # Get top players by average percentage
        rows = conn.execute(
            """
            SELECT 
                p.id,
                p.username,
                COUNT(s.id) as games_played,
                SUM(s.score) as total_score,
                SUM(s.total_questions) as total_questions,
                AVG(s.percentage) as avg_percentage,
                MAX(s.percentage) as best_percentage
            FROM players p
            JOIN scores s ON p.id = s.player_id
            GROUP BY p.id
            HAVING games_played >= 1
            ORDER BY avg_percentage DESC, total_score DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()
        
        conn.close()
        
        leaderboard = []
        for idx, row in enumerate(rows, 1):
            leaderboard.append({
                "rank": idx,
                "player_id": row["id"],
                "username": row["username"],
                "games_played": row["games_played"],
                "total_score": row["total_score"],
                "total_questions": row["total_questions"],
                "avg_percentage": round(row["avg_percentage"], 2),
                "best_percentage": round(row["best_percentage"], 2)
            })
        
        return jsonify(leaderboard)
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch leaderboard", "details": str(e)}), 500

@scoreboard_bp.route("/leaderboard/category/<category>")
def get_category_leaderboard(category):
    """Get leaderboard for a specific category"""
    try:
        limit = request.args.get("limit", 100, type=int)
        
        conn = get_db()
        
        rows = conn.execute(
            """
            SELECT 
                p.id,
                p.username,
                COUNT(s.id) as games_played,
                SUM(s.score) as total_score,
                SUM(s.total_questions) as total_questions,
                AVG(s.percentage) as avg_percentage,
                MAX(s.percentage) as best_percentage
            FROM players p
            JOIN scores s ON p.id = s.player_id
            WHERE s.category = ?
            GROUP BY p.id
            ORDER BY avg_percentage DESC, total_score DESC
            LIMIT ?
            """,
            (category, limit)
        ).fetchall()
        
        conn.close()
        
        leaderboard = []
        for idx, row in enumerate(rows, 1):
            leaderboard.append({
                "rank": idx,
                "player_id": row["id"],
                "username": row["username"],
                "games_played": row["games_played"],
                "total_score": row["total_score"],
                "total_questions": row["total_questions"],
                "avg_percentage": round(row["avg_percentage"], 2),
                "best_percentage": round(row["best_percentage"], 2)
            })
        
        return jsonify(leaderboard)
        
    except Exception as e:
        return jsonify({"error": "Failed to fetch category leaderboard", "details": str(e)}), 500
