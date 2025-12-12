# Vercel Deployment Guide

This guide will help you deploy TriviaQuest to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Your backend API deployed and accessible (see Backend Deployment section)
3. Git repository with your code

## Frontend Deployment on Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub/GitLab/Bitbucket**
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Import Project on Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your Git repository
   - **Important**: Set the "Root Directory" to `frontend` in project settings, OR
   - Vercel will use the root `vercel.json` which is configured for the frontend directory
   - The build will automatically run from the `frontend` directory

3. **Configure Environment Variables**
   - In your Vercel project settings, go to "Environment Variables"
   - Add the following variable:
     - **Name**: `VITE_API_BASE_URL`
     - **Value**: Your backend API URL (e.g., `https://your-backend.railway.app`)
   - Make sure to add it for all environments (Production, Preview, Development)

4. **Deploy**
   - Click "Deploy"
   - Vercel will automatically build and deploy your frontend

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Set Environment Variables**
   ```bash
   vercel env add VITE_API_BASE_URL
   # Enter your backend URL when prompted
   ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Backend Deployment

Since your backend is a Flask application, you'll need to deploy it separately. Here are recommended options:

### Option 1: Railway (Recommended for Flask)

1. Sign up at [railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Add a new service and select "Deploy from GitHub repo"
5. Select the `backend` directory
6. Railway will auto-detect Python and install dependencies
7. Set the start command: `python app.py` or `gunicorn app:app`
8. Your backend will get a URL like `https://your-app.railway.app`
9. Use this URL as your `VITE_API_BASE_URL` in Vercel

### Option 2: Render

1. Sign up at [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your repository
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Root Directory**: `backend`
5. Deploy and use the provided URL

### Option 3: Heroku

1. Install Heroku CLI
2. Create a `Procfile` in the backend directory:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku create your-app-name
   git subtree push --prefix backend heroku main
   ```

## Environment Variables

### Frontend (Vercel)
- `VITE_API_BASE_URL`: Your backend API URL

### Backend (Railway/Render/etc.)
- Database configuration (if using external database)
- Any other backend-specific environment variables

## Database Setup

If you're using SQLite (default), note that:
- SQLite files are ephemeral on most hosting platforms
- Consider migrating to PostgreSQL for production:
  1. Update your backend to use PostgreSQL
  2. Set up a PostgreSQL database on Railway/Render
  3. Update connection strings in environment variables

## Post-Deployment Checklist

- [ ] Frontend deployed on Vercel
- [ ] Backend deployed and accessible
- [ ] Environment variables configured
- [ ] CORS configured on backend to allow Vercel domain
- [ ] Test all API endpoints
- [ ] Verify database migrations are run
- [ ] Test the full application flow

## Troubleshooting

### CORS Errors
If you see CORS errors, make sure your Flask backend has CORS configured:
```python
from flask_cors import CORS
CORS(app, origins=["https://your-vercel-app.vercel.app"])
```

### API Connection Issues
- Verify `VITE_API_BASE_URL` is set correctly in Vercel
- Check that your backend is accessible from the internet
- Verify CORS settings allow your Vercel domain

### Build Errors
- Check that all dependencies are in `package.json`
- Verify Node.js version compatibility
- Check Vercel build logs for specific errors

## Custom Domain

To add a custom domain:
1. Go to your Vercel project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Continuous Deployment

Vercel automatically deploys on every push to your main branch. For preview deployments, every pull request gets its own deployment URL.

