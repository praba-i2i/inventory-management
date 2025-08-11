# Railway Deployment Guide

This guide will help you deploy the backend service to Railway with PostgreSQL.

## Prerequisites

1. Railway account (https://railway.app)
2. Git repository with your code

## Deployment Steps

### 1. Create a New Project on Railway

1. Go to Railway dashboard
2. Click "New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository

### 2. Add PostgreSQL Database (CRITICAL STEP)

1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a PostgreSQL database
4. **IMPORTANT**: After creating the database, go to the database service
5. Click on "Connect" tab
6. Copy the "Postgres Connection URL" - this is your `DATABASE_URL`

### 3. Connect Database to Your Service

1. Go back to your main service (the one running your code)
2. Go to "Variables" tab
3. Add a new variable:
   - **Name**: `DATABASE_URL`
   - **Value**: Paste the Postgres Connection URL from step 2
4. Click "Add"
5. Your service will automatically redeploy

### 4. Configure Other Environment Variables

In your Railway project settings, add these environment variables:

```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
```

### 5. Deploy the Service

1. Railway will automatically detect the Python application
2. The build process will:
   - Install Python 3.11 and dependencies
   - Start the application using the Dockerfile

### 6. Get Your Public URL

1. After deployment, go to your service
2. Click on "Settings" tab
3. Scroll down to "Domains" section
4. Click "Generate Domain" to get a public URL
5. Or use the default Railway domain

### 7. Verify Deployment

1. Check the deployment logs in Railway dashboard
2. Visit your service URL + `/health` to verify the API is running
3. Visit `/debug` to check environment variables
4. The API will be available at: `https://your-app-name.railway.app/api/v1/`

## Configuration Files

The following files have been added for Railway deployment:

### Docker Deployment:
- `Dockerfile` - Container configuration
- `.dockerignore` - Files to exclude from Docker build
- `requirements.txt` - Python dependencies (includes email-validator)

### Common:
- `.railwayignore` - Files to exclude from deployment
- `entrypoint.sh` - Startup script with debugging

## Troubleshooting

### Database Connection Issues:
1. **"DATABASE_URL=NOT SET"**: You need to manually add the DATABASE_URL variable
2. **"Connection refused"**: Make sure you've created a PostgreSQL database in Railway
3. **SSL errors**: The configuration automatically handles Railway's SSL requirements

### No Public URL:
1. **Check Settings**: Go to your service → Settings → Domains
2. **Generate Domain**: Click "Generate Domain" to get a public URL
3. **Custom Domain**: You can also add your own custom domain

### General Issues:
1. **Build fails**: Check the Railway logs for specific error messages
2. **Port issues**: Railway automatically sets the PORT environment variable
3. **CORS issues**: The configuration allows all origins for now, adjust as needed

## Database Migration

The application will automatically create database tables on startup using SQLAlchemy's `create_all()` method. For production, you might want to use Alembic migrations instead.

## API Endpoints

Once deployed, your API will be available at:
- Health check: `https://your-app-name.railway.app/health`
- Debug info: `https://your-app-name.railway.app/debug`
- API docs: `https://your-app-name.railway.app/api/v1/docs`
- API root: `https://your-app-name.railway.app/api/v1/`

## Recent Fixes

- **Fixed email-validator dependency**: Added missing package for Pydantic EmailStr
- **Fixed container startup issue**: Created entrypoint script for proper startup
- **Added Docker deployment**: More reliable than Nixpacks
- **Enhanced debugging**: Added debug endpoint and better logging
- **Updated Python version**: Using Python 3.11.7 for better stability
