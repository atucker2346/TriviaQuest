from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.questions import questions_bp
from routes.scoreboard.Scoreboard import scoreboard_bp
from routes.daily_challenges import daily_challenges_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(questions_bp)
app.register_blueprint(scoreboard_bp)
app.register_blueprint(daily_challenges_bp)

# Serve static files (sound effects)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)