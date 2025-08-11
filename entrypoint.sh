#!/bin/bash
set -e

echo "=== Railway Entrypoint Script ==="
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

echo "Environment variables:"
echo "PORT: $PORT"
echo "DATABASE_URL: ${DATABASE_URL:+SET}"
echo "PYTHONPATH: $PYTHONPATH"

# Test environment variables with Python
echo "Testing environment variables with Python:"
python test_env.py

echo "Changing to backend directory..."
cd backend
echo "Backend directory contents:"
ls -la

# Run database migrations if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    echo "Running database migrations..."
    echo "Current directory before migration: $(pwd)"
    echo "Checking if run_migrations.py exists:"
    ls -la run_migrations.py
    
    python run_migrations.py
    migration_exit_code=$?
    
    if [ $migration_exit_code -eq 0 ]; then
        echo "✅ Database migrations completed successfully"
    else
        echo "⚠️  Database migrations failed (exit code: $migration_exit_code), but continuing..."
    fi
else
    echo "⚠️  DATABASE_URL not set, skipping migrations"
fi

echo "Starting Python application..."
exec python main.py
