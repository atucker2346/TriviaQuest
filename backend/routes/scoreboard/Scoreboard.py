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

def ensure_schema(conn):
    """Create required tables/columns if they don't exist"""
    cursor = conn.cursor()

    # Players table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Scores table with optional time/hints columns
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            time_taken INTEGER,
            hints_used INTEGER DEFAULT 0,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players(id)
        )
        """
    )

    # Backfill columns if table existed without them
    try:
        cursor.execute("ALTER TABLE scores ADD COLUMN time_taken INTEGER")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE scores ADD COLUMN hints_used INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # Helpful indexes
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_scores_player_id ON scores(player_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_scores_played_at ON scores(played_at DESC)"
    )

    conn.commit()

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
        ensure_schema(conn)
        
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
        time_taken = data.get("time_taken", 0)
        hints_used = data.get("hints_used", 0)
        
        if not all([player_id, category, score is not None, total_questions]):
            return jsonify({"error": "Missing required fields"}), 400
        
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        conn = get_db()
        cursor = conn.cursor()
        ensure_schema(conn)
        
        cursor.execute(
            """
            INSERT INTO scores (player_id, category, score, total_questions, percentage, time_taken, hints_used)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (player_id, category, score, total_questions, percentage, time_taken, hints_used)
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

        # Get total time
        total_time_taken = conn.execute(
            "SELECT SUM(time_taken) as total FROM scores WHERE player_id = ?",
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

        # Fastest average time per question (only for games with time data)
        fastest_time_row = conn.execute(
            """
            SELECT MIN(time_taken * 1.0 / total_questions) as best_time_per_question
            FROM scores
            WHERE player_id = ? AND time_taken IS NOT NULL AND total_questions > 0
            """,
            (player_id,)
        ).fetchone()
        best_time_per_question = fastest_time_row["best_time_per_question"] if fastest_time_row else None
        
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
                "average_percentage": round(avg_percentage, 2),
                "average_time_per_question": round(total_time_taken / total_questions, 2) if total_questions and total_time_taken else None
            },
            "best_score": dict(best_score) if best_score else None,
            "best_time_per_question": round(best_time_per_question, 2) if best_time_per_question else None,
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
        
        # Get top players by average percentage and speed
        rows = conn.execute(
            """
            SELECT 
                p.id,
                p.username,
                COUNT(s.id) as games_played,
                SUM(s.score) as total_score,
                SUM(s.total_questions) as total_questions,
                SUM(CASE WHEN s.time_taken IS NOT NULL THEN s.time_taken ELSE 0 END) as total_time_taken,
                AVG(s.percentage) as avg_percentage,
                MAX(s.percentage) as best_percentage,
                MIN(CASE WHEN s.time_taken IS NOT NULL AND s.total_questions > 0 THEN (s.time_taken * 1.0 / s.total_questions) END) as best_time_per_question
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
            total_questions = row["total_questions"] or 0
            total_time_taken = row["total_time_taken"] or 0
            avg_time_per_question = None
            if total_questions > 0 and total_time_taken > 0:
                avg_time_per_question = round(total_time_taken / total_questions, 2)

            best_time_per_question = None
            if row["best_time_per_question"] is not None:
                best_time_per_question = round(row["best_time_per_question"], 2)

            leaderboard.append({
                "rank": idx,
                "player_id": row["id"],
                "username": row["username"],
                "games_played": row["games_played"],
                "total_score": row["total_score"],
                "total_questions": row["total_questions"],
                "avg_percentage": round(row["avg_percentage"], 2),
                "best_percentage": round(row["best_percentage"], 2),
                "avg_time_per_question": avg_time_per_question,
                "best_time_per_question": best_time_per_question
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
