#!/usr/bin/env python3
"""
Standalone script to run database migrations
"""
import os
import sys
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    """Run Alembic migrations"""
    try:
        # Check if DATABASE_URL is set
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            logger.error("DATABASE_URL environment variable is not set!")
            return False
        
        logger.info("Running database migrations...")
        logger.info(f"Database URL: {database_url[:20]}...")
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Python executable: {sys.executable}")
        
        # Check if alembic.ini exists
        if not os.path.exists("alembic.ini"):
            logger.error("alembic.ini not found in current directory!")
            logger.info(f"Files in current directory: {os.listdir('.')}")
            return False
        
        # Run alembic upgrade
        logger.info("Executing: alembic upgrade head")
        result = subprocess.run([
            sys.executable, '-m', 'alembic', 'upgrade', 'head'
        ], capture_output=True, text=True, check=True)
        
        logger.info("✅ Migrations completed successfully")
        logger.info(f"Migration output: {result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Migration failed: {e}")
        logger.error(f"Migration error output: {e.stderr}")
        logger.error(f"Migration return code: {e.returncode}")
        return False
    except Exception as e:
        logger.error(f"❌ Error running migrations: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
