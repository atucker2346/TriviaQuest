from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from routes.questions import questions_bp
from routes.scoreboard.Scoreboard import scoreboard_bp
from routes.daily_challenges import daily_challenges_bp
from routes.challenges import challenges_bp

app = Flask(__name__)

# Configure CORS - allow all origins in production, or specific origins from env
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, origins=cors_origins)
app.register_blueprint(questions_bp)
app.register_blueprint(scoreboard_bp)
app.register_blueprint(daily_challenges_bp)
app.register_blueprint(challenges_bp)

# Serve static files (sound effects)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)