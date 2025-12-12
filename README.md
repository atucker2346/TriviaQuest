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

## Deployment

### Frontend (Vercel)

The frontend is configured for deployment on Vercel. See [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md) for detailed instructions.

Quick steps:
1. Push your code to GitHub
2. Import the project on Vercel
3. Set the root directory to `frontend` (or use the root `vercel.json`)
4. Add environment variable: `VITE_API_BASE_URL` = your backend URL
5. Deploy!

### Backend

The backend can be deployed on Railway, Render, Heroku, or any Python hosting service. See [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md) for backend deployment options.

**Important**: Make sure to:
- Configure CORS to allow your Vercel domain
- Set up environment variables (especially `CORS_ORIGINS` if restricting origins)
- Run database migrations if needed

