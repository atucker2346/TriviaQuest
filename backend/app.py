from flask import Flask
from flask_cors import CORS
from routes.questions import questions_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(questions_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
