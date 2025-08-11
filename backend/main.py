from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.models import Base
import logging
import os
import subprocess
import sys
from contextlib import asynccontextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if DATABASE_URL is set before importing database modules
DATABASE_URL = os.getenv("DATABASE_URL")
logger.info(f"Raw DATABASE_URL from os.getenv: {DATABASE_URL}")

if not DATABASE_URL:
    logger.error("DATABASE_URL environment variable is not set!")
    logger.error("Please set the DATABASE_URL environment variable in Railway")
    # Import database modules only if DATABASE_URL is set
    engine = None
    test_db_connection = lambda: False
else:
    from app.core.database import engine, test_db_connection

def run_migrations():
    """Run Alembic migrations"""
    try:
        logger.info("Running database migrations...")
        # Change to the backend directory where alembic.ini is located
        os.chdir(os.path.join(os.getcwd(), 'backend'))
        
        # Run alembic upgrade
        result = subprocess.run([
            sys.executable, '-m', 'alembic', 'upgrade', 'head'
        ], capture_output=True, text=True, check=True)
        
        logger.info("Migrations completed successfully")
        logger.info(f"Migration output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        logger.error(f"Migration error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI"""
    # Startup
    logger.info("Starting application...")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Files in current directory: {os.listdir('.')}")
    
    # Test database connection first
    if DATABASE_URL and test_db_connection():
        try:
            logger.info("Database connection successful, running migrations...")
            # Run migrations
            if run_migrations():
                logger.info("Database migrations completed successfully")
            else:
                logger.warning("Database migrations failed, but continuing...")
            
            # Create tables as fallback (in case migrations don't cover everything)
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to setup database: {e}")
    else:
        logger.warning("Database connection failed during startup, but continuing...")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title="Inventory Management API",
    description="A comprehensive inventory management system API",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to Inventory Management API"}

@app.get("/test")
async def test():
    """Simple test endpoint"""
    return {"message": "Test endpoint working", "timestamp": "now"}

@app.get("/api-test")
async def api_test():
    """Test API routing"""
    return {"message": "API routing is working", "endpoint": "/api-test"}

@app.get("/health")
async def health_check():
    """Simple health check endpoint for Railway - doesn't check database"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/health/db")
async def health_check_db():
    """Database health check endpoint"""
    if not DATABASE_URL:
        return {"status": "unhealthy", "message": "DATABASE_URL not set"}, 503
    
    if test_db_connection():
        return {"status": "healthy", "message": "Database is connected"}
    else:
        return {"status": "unhealthy", "message": "Database connection failed"}, 503

@app.get("/debug")
async def debug_info():
    """Debug endpoint to check environment and configuration"""
    return {
        "port": os.getenv("PORT", "NOT SET"),
        "database_url_set": bool(os.getenv("DATABASE_URL")),
        "database_url_preview": os.getenv("DATABASE_URL", "NOT SET")[:20] + "..." if os.getenv("DATABASE_URL") else "NOT SET",
        "python_path": os.getenv("PYTHONPATH", "NOT SET"),
        "current_dir": os.getcwd(),
        "files_in_dir": os.listdir(".") if os.path.exists(".") else [],
        "backend_files": os.listdir("backend") if os.path.exists("backend") else [],
        "settings_port": settings.PORT,
        "settings_database_url_set": bool(settings.DATABASE_URL),
        "settings_database_url_preview": settings.DATABASE_URL[:20] + "..." if settings.DATABASE_URL else "NOT SET",
        "raw_database_url": DATABASE_URL if DATABASE_URL else "NOT SET"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Use settings PORT (which should be set from environment variable)
    port = settings.PORT
    logger.info(f"Starting server on port {port}")
    logger.info(f"Environment variables: PORT={os.getenv('PORT')}, DATABASE_URL={'SET' if os.getenv('DATABASE_URL') else 'NOT SET'}")
    logger.info(f"Settings PORT: {settings.PORT}")
    logger.info(f"Settings DATABASE_URL set: {bool(settings.DATABASE_URL)}")
    logger.info(f"Settings DATABASE_URL preview: {settings.DATABASE_URL[:20] + '...' if settings.DATABASE_URL else 'NOT SET'}")
    
    if not DATABASE_URL:
        logger.error("⚠️  WARNING: DATABASE_URL is not set! Database features will not work.")
        logger.error("Please set the DATABASE_URL environment variable in Railway")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
