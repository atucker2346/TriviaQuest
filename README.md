# TriviaQuest

A trivia quiz application with a Flask backend and React frontend.

## Project Structure

```
TriviaQuest/
├── backend/          # Flask API server
│   ├── app.py       # Main Flask application
│   ├── routes/      # API routes
│   └── questions.db # SQLite database
└── frontend/        # React frontend application
    ├── src/         # React source files
    └── package.json # Frontend dependencies
```

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies (you may need to install flask-cors):
```bash
pip install flask flask-cors
```

3. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Start the backend server first
2. Start the frontend development server
3. Open `http://localhost:3000` in your browser
4. Select a category and start answering trivia questions!

