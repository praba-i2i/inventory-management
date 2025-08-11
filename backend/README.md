# Inventory Management System - Backend

A comprehensive FastAPI backend for managing inventory, products, suppliers, purchase orders, and stock alerts.

## 🚀 Core Features

### 1. Product Catalog
- **Products**: Manage products with categories, specifications, and supplier information
- **Categories**: Organize products into categories
- **Specifications**: Flexible JSON-based product specifications
- **Pricing**: Cost and selling price management
- **Product Status**: Active/inactive and featured product flags

### 2. Inventory Tracking
- **Multi-location Support**: Track stock across multiple warehouses/locations
- **Stock Levels**: Real-time quantity tracking with reserved and available quantities
- **Storage Information**: Shelf/zone location tracking
- **Cost Valuation**: Automatic total value calculations
- **Stock Thresholds**: Reorder levels and maximum stock levels

### 3. Purchase Orders
- **Order Management**: Create, update, and track purchase orders
- **Supplier Integration**: Link orders to suppliers
- **Status Tracking**: Draft → Pending Approval → Approved → Ordered → Received
- **Financial Tracking**: Subtotal, tax, shipping, and total amounts
- **Item Management**: Multiple items per order with quantities and pricing

### 4. Stock Alerts
- **Alert Types**: Low stock, out of stock, overstock, expiry warnings
- **Severity Levels**: Low, medium, high, critical
- **Status Management**: Active, acknowledged, resolved, dismissed
- **Notification Tracking**: Email and SMS notification status
- **Resolution Tracking**: Who resolved and when

## 🏗️ Architecture

### Database Models
```
├── categories/          # Product categories
├── products/           # Product catalog with specifications
├── suppliers/          # Supplier information
├── locations/          # Warehouse/location management
├── inventory_items/    # Stock tracking across locations
├── purchase_orders/    # Purchase order management
├── purchase_order_items/ # Order line items
└── stock_alerts/      # Stock alert system
```

### API Endpoints

#### Products (`/api/v1/products/`)
- `GET /` - List all products with filtering
- `GET /with-inventory` - Products with inventory information
- `GET /{id}` - Get specific product
- `POST /` - Create new product
- `PUT /{id}` - Update product
- `DELETE /{id}` - Delete product

#### Inventory (`/api/v1/inventory/`)
- `GET /` - List inventory items with filtering
- `GET /summary` - Inventory summary statistics
- `GET /{id}` - Get specific inventory item
- `POST /` - Create inventory item
- `PUT /{id}` - Update inventory item
- `DELETE /{id}` - Delete inventory item
- `POST /{id}/adjust` - Adjust inventory quantity

#### Categories (`/api/v1/categories/`)
- `GET /` - List categories
- `GET /{id}` - Get specific category
- `POST /` - Create category
- `PUT /{id}` - Update category
- `DELETE /{id}` - Delete category

#### Items (Legacy) (`/api/v1/items/`)
- `GET /` - List items
- `GET /{id}` - Get specific item
- `POST /` - Create item
- `PUT /{id}` - Update item
- `DELETE /{id}` - Delete item

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip

### Installation

1. **Clone and navigate to backend directory**
```bash
cd backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file with your configuration
DATABASE_URL=postgresql://postgres:rapid@localhost:5432/inventory
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
```

4. **Run database migrations**
```bash
# Initialize Alembic (first time only)
alembic init alembic

# Run migrations
alembic upgrade head
```

5. **Start the server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Database Schema

### Key Relationships
- **Products** belong to **Categories** and optionally to **Suppliers**
- **Inventory Items** link **Products** to **Locations**
- **Purchase Orders** belong to **Suppliers** and contain **Purchase Order Items**
- **Stock Alerts** link **Products** to **Locations** with alert information

### Migration Management
```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check current migration
alembic current
```

## 🔧 Configuration

### Environment Variables
```env
DATABASE_URL=postgresql://postgres:rapid@localhost:5432/inventory
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=480
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
DEBUG=true
```

### Database Configuration
- **Host**: localhost
- **Port**: 5432
- **Database**: inventory
- **Username**: postgres
- **Password**: rapid

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Run Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 🔍 Key Features Explained

### Product Catalog
- **Flexible Specifications**: JSON field for product specifications
- **Pricing Management**: Separate cost and selling prices
- **Supplier Integration**: Link products to suppliers
- **Status Management**: Active/inactive and featured flags

### Inventory Tracking
- **Multi-location**: Track same product across multiple locations
- **Quantity Types**: Total, reserved, and available quantities
- **Automatic Calculations**: Available quantity = Total - Reserved
- **Value Tracking**: Automatic total value calculation

### Purchase Orders
- **Workflow Management**: Status-based order progression
- **Financial Tracking**: Comprehensive cost breakdown
- **Supplier Integration**: Full supplier information
- **Item Management**: Multiple items with individual pricing

### Stock Alerts
- **Multiple Alert Types**: Low stock, out of stock, overstock, etc.
- **Severity Management**: Prioritize alerts by importance
- **Status Tracking**: Track alert lifecycle
- **Notification Integration**: Email and SMS tracking

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Use proper production values
2. **Database**: Use production PostgreSQL instance
3. **Security**: Change default secret keys
4. **CORS**: Configure allowed origins
5. **Logging**: Set up proper logging configuration

### Docker Deployment
```bash
# Build image
docker build -f ../Dockerfile.backend -t inventory-backend .

# Run container
docker run -p 8000:8000 inventory-backend
```

## 📝 Development

### Code Structure
```
backend/
├── app/
│   ├── api/              # API routes
│   ├── core/             # Core configuration
│   ├── models/           # Database models
│   └── schemas/          # Pydantic schemas
├── alembic/              # Database migrations
├── main.py              # Application entry point
└── requirements.txt     # Dependencies
```

### Adding New Features
1. Create database models in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Create API endpoints in `app/api/api_v1/endpoints/`
4. Add routes to `app/api/api_v1/api.py`
5. Create and run migrations

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper type hints
3. Include docstrings for functions
4. Write tests for new features
5. Update API documentation

## 📄 License

This project is licensed under the MIT License.
