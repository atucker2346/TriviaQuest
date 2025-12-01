# TriviaQuest Quick Start

## ✅ Setup Complete!

The application has been set up on your laptop. Here's how to run it:

## Running the Application

### Option 1: Use the Background Servers (Already Started)

The servers may already be running in the background. Simply open your browser and go to:
**http://localhost:3000**

### Option 2: Manual Start

If you need to restart the servers, use these commands:

#### Backend Server (Terminal 1)
```powershell
cd backend
&"C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python312\python.exe" app.py
```
The backend will run on `http://localhost:5001`

#### Frontend Server (Terminal 2)
```powershell
cd frontend
&"C:\Program Files\nodejs\npm.cmd" run dev
```
The frontend will run on `http://localhost:3000`

## Access the Application

1. Make sure both servers are running
2. Open your web browser
3. Navigate to **http://localhost:3000**
4. Select a category and start answering trivia questions!

## What Was Set Up

- ✅ Python 3.12 installed
- ✅ Flask and flask-cors installed
- ✅ Database created and seeded with 50 questions (10 per category)
- ✅ Node.js found and configured
- ✅ Frontend dependencies installed
- ✅ Backend server started on port 5001
- ✅ Frontend server started on port 3000

## Troubleshooting

- If the frontend shows connection errors, make sure the backend is running on port 5001
- If you see "port already in use" errors, close any existing servers first
- To stop servers, press `Ctrl+C` in the terminal windows

## Categories Available

- General Knowledge
- Science
- History
- Pop Culture
- Sports

Enjoy your trivia quiz!

