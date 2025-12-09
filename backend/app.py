from flask import Flask
from flask_cors import CORS
from routes.questions import questions_bp
from routes.scoreboard.Scoreboard import scoreboard_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(questions_bp)
app.register_blueprint(scoreboard_bp)

if __name__ == '__main__':
    app.run(port=5001, debug=True)