# Database Migrations Guide

This guide explains how database migrations are automatically run during Railway deployment.

## Migration Setup

Your inventory management service is configured to automatically run database migrations during deployment using Alembic.

## How It Works

### 1. **Automatic Migration Execution**
- Migrations run automatically when the application starts
- The `entrypoint.sh` script runs `run_migrations.py` before starting the application
- The FastAPI lifespan event also runs migrations as a backup

### 2. **Migration Files**
- **Location**: `backend/alembic/versions/`
- **Current Migration**: `001_initial_schema.py` (creates all initial tables)
- **Configuration**: `backend/alembic.ini` and `backend/alembic/env.py`

### 3. **Migration Scripts**
- **`run_migrations.py`**: Standalone script to run migrations manually
- **`entrypoint.sh`**: Runs migrations during container startup
- **`main.py`**: Runs migrations in the FastAPI lifespan event

## Migration Process

### During Deployment:
1. **Container starts** → `entrypoint.sh` executes
2. **Environment check** → Verifies `DATABASE_URL` is set
3. **Migration execution** → Runs `python run_migrations.py`
4. **Application startup** → FastAPI starts with database ready

### Migration Commands:
```bash
# Run migrations to latest version
alembic upgrade head

# Check current migration status
alembic current

# Create a new migration
alembic revision --autogenerate -m "description"

# Rollback to previous version
alembic downgrade -1
```

## Manual Migration Execution

If you need to run migrations manually:

### Using Railway CLI:
```bash
# Connect to your Railway project
railway login
railway link

# Run migrations manually
railway run python backend/run_migrations.py
```

### Using Railway Web Interface:
1. Go to your Railway project dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click "Deploy" to trigger a new deployment with migrations

## Migration Status

You can check migration status by visiting:
- **Health Check**: `https://inventory-management-production-82d5.up.railway.app/health`
- **Database Health**: `https://inventory-management-production-82d5.up.railway.app/health/db`
- **Debug Info**: `https://inventory-management-production-82d5.up.railway.app/debug`

## Creating New Migrations

When you make changes to your models:

1. **Update your SQLAlchemy models** in `backend/app/models/`
2. **Generate migration**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "description of changes"
   ```
3. **Review the generated migration** in `backend/alembic/versions/`
4. **Deploy to Railway** - migrations will run automatically

## Troubleshooting

### Migration Fails:
1. **Check logs** in Railway dashboard
2. **Verify DATABASE_URL** is set correctly
3. **Check database connection** using `/health/db` endpoint
4. **Review migration files** for syntax errors

### Tables Not Created:
1. **Check migration status** in logs
2. **Verify models are imported** in `alembic/env.py`
3. **Check for migration conflicts**

### Manual Migration Recovery:
```bash
# Connect to Railway and run migrations manually
railway run python backend/run_migrations.py

# Or run specific migration
railway run alembic upgrade head
```

## Database Schema

Your current migration creates these tables:
- `categories` - Product categories
- `items` - Basic items
- `products` - Products with supplier and category relationships
- `suppliers` - Product suppliers
- `locations` - Storage locations
- `inventory_items` - Inventory tracking
- `purchase_orders` - Purchase orders
- `purchase_order_items` - Items in purchase orders
- `stock_alerts` - Low stock alerts

## Best Practices

1. **Always test migrations locally** before deploying
2. **Use descriptive migration names** when creating new ones
3. **Review auto-generated migrations** before applying
4. **Keep migrations small and focused**
5. **Backup database** before major schema changes

## Environment Variables

Required for migrations:
- `DATABASE_URL` - PostgreSQL connection string (set by Railway)

The migration system will automatically:
- Use Railway's PostgreSQL database
- Apply SSL mode for secure connections
- Handle connection pooling and timeouts
