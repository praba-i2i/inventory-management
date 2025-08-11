#!/bin/bash
set -e

echo "Starting Inventory Management API..."
echo "Current directory: $(pwd)"
echo "Contents: $(ls -la)"

# Change to backend directory
cd backend
echo "Changed to backend directory: $(pwd)"
echo "Backend contents: $(ls -la)"

# Wait a moment for any system services to be ready
echo "Waiting for system to be ready..."
sleep 5

# Run the Python application
echo "Starting Python application..."
exec python main.py
