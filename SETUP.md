# TriviaQuest Setup Guide

## Prerequisites

You need to install the following before running the application:

### 1. Install Python

1. Download Python from https://www.python.org/downloads/
2. During installation, **check the box** "Add Python to PATH"
3. Verify installation by opening a new terminal and running:
   ```powershell
   python --version
   ```

### 2. Install Node.js

1. Download Node.js from https://nodejs.org/ (LTS version recommended)
2. Run the installer with default settings
3. Verify installation by opening a new terminal and running:
   ```powershell
   node --version
   npm --version
   ```

## Setup Steps

### Backend Setup

1. Open a terminal and navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Install Python dependencies:
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Set up the database:
   ```powershell
   python setup_db.py
   python seed_questions.py
   ```

4. Start the Flask server:
   ```powershell
   python app.py
   ```
   
   The backend will run on `http://localhost:5001`

### Frontend Setup

1. Open a **new terminal** and navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Start the development server:
   ```powershell
   npm run dev
   ```
   
   The frontend will run on `http://localhost:3000`

## Running the Application

1. **First**, start the backend server (keep it running)
2. **Then**, start the frontend server (keep it running)
3. Open your browser and go to `http://localhost:3000`
4. Select a category and start answering trivia questions!

## Troubleshooting

- If Python is not recognized, make sure it's added to your PATH
- If Node.js is not recognized, restart your terminal after installation
- Make sure both servers are running before accessing the frontend
- If you see CORS errors, ensure the backend is running on port 5001

