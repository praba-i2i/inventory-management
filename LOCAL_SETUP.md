# Local Development Setup (Without Docker)

This guide will help you set up and run the Inventory Management System locally without Docker.

## Prerequisites

1. **Python 3.8+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download here](https://nodejs.org/)
3. **PostgreSQL 12+** - [Download here](https://www.postgresql.org/download/)

## Step 1: PostgreSQL Setup

### Install PostgreSQL
1. Download and install PostgreSQL from the official website
2. During installation, set the password for the `postgres` user to `rapid`
3. Keep the default port as `5432`

### Create Database and Tables
1. Open pgAdmin or use psql command line
2. Connect to PostgreSQL as the `postgres` user
3. Run the setup script:

```bash
# Using psql command line
psql -U postgres -f setup_local_db.sql

# Or using pgAdmin
# Open the setup_local_db.sql file and execute it
```

### Alternative: Manual Database Setup
If you prefer to set up manually:

```sql
-- Connect to PostgreSQL as postgres user
-- Create database
CREATE DATABASE inventory;

-- Connect to the inventory database
\c inventory;

-- Run the contents of setup_local_db.sql
```

## Step 2: Backend Setup

### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Start Backend Server
```bash
# Option 1: Using the provided script
start_backend.bat

# Option 2: Manual command
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs

## Step 3: Frontend Setup

### Install Node.js Dependencies
```bash
cd frontend
npm install
```

### Start Frontend Server
```bash
# Option 1: Using the provided script
start_frontend.bat

# Option 2: Manual command
cd frontend
npm start
```

The frontend will be available at:
- **Application**: http://localhost:3000

## Step 4: Verify Setup

1. **Backend Health Check**: Visit http://localhost:8000/health
2. **API Documentation**: Visit http://localhost:8000/docs
3. **Frontend**: Visit http://localhost:3000

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify the password is set to `rapid`
- Check that the `inventory` database exists
- Verify the connection string in `backend/app/core/config.py`

### Port Conflicts
- Backend uses port 8000
- Frontend uses port 3000
- PostgreSQL uses port 5432
- If any port is in use, change it in the respective configuration

### Python Dependencies
If you encounter issues with Python packages:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with specific Python version
python3 -m pip install -r requirements.txt
```

### Node.js Dependencies
If you encounter issues with Node.js packages:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## Development Workflow

1. **Start PostgreSQL** (ensure it's running)
2. **Start Backend**: Run `start_backend.bat` or `uvicorn main:app --reload`
3. **Start Frontend**: Run `start_frontend.bat` or `npm start`
4. **Access Application**: Open http://localhost:3000

## Environment Variables

The application uses the following default configurations:
- **Database**: `postgresql://postgres:rapid@localhost:5432/inventory`
- **Backend Port**: 8000
- **Frontend Port**: 3000
- **API Base URL**: http://localhost:8000

## Stopping Services

- **Backend**: Press `Ctrl+C` in the backend terminal
- **Frontend**: Press `Ctrl+C` in the frontend terminal
- **PostgreSQL**: Stop the PostgreSQL service from your system services
