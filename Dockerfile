FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY entrypoint.sh ./
COPY test_env.py ./

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose port (Railway will override this)
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Test environment variables during build
RUN python test_env.py

# Run the application using entrypoint script
CMD ["./entrypoint.sh"]
