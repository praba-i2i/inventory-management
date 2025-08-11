# Development Prompts - Inventory Management System

## Overview
This document contains the development prompts and requirements used to build the Inventory Management System. These prompts guided the development process and can be used for future enhancements or similar projects.

## Initial Project Setup Prompts

### 1. Project Initialization
```
Create a comprehensive inventory management system with the following requirements:

Backend:
- FastAPI with Python 3.11
- PostgreSQL database with SQLAlchemy ORM
- Alembic for database migrations
- Pydantic for data validation
- RESTful API endpoints
- CORS support
- Docker containerization

Frontend:
- React 18 with TypeScript
- Tailwind CSS for styling
- React Router for navigation
- Axios for API communication
- Responsive design
- Modern UI/UX

Features:
- Product management (CRUD operations)
- Category management
- Supplier management
- Location management
- Inventory tracking
- Purchase orders
- Stock alerts
- Dashboard with analytics

Deployment:
- Railway for hosting
- PostgreSQL database on Railway
- Automatic migrations
- Environment variable management
```

### 2. Database Design
```
Design a comprehensive database schema for an inventory management system with the following entities:

1. Categories
   - id (Primary Key)
   - name (VARCHAR, NOT NULL)
   - description (TEXT)
   - created_at, updated_at timestamps

2. Suppliers
   - id (Primary Key)
   - name (VARCHAR, NOT NULL)
   - email (VARCHAR)
   - phone (VARCHAR)
   - address (TEXT)
   - contact_person (VARCHAR)
   - created_at, updated_at timestamps

3. Locations
   - id (Primary Key)
   - name (VARCHAR, NOT NULL)
   - address (TEXT)
   - description (TEXT)
   - created_at, updated_at timestamps

4. Products
   - id (Primary Key)
   - name (VARCHAR, NOT NULL)
   - description (TEXT)
   - sku (VARCHAR, UNIQUE, NOT NULL)
   - price (DECIMAL)
   - cost (DECIMAL)
   - category_id (Foreign Key to Categories)
   - supplier_id (Foreign Key to Suppliers)
   - is_active (BOOLEAN, DEFAULT TRUE)
   - created_at, updated_at timestamps

5. Inventory
   - id (Primary Key)
   - product_id (Foreign Key to Products)
   - location_id (Foreign Key to Locations)
   - quantity (INTEGER, DEFAULT 0)
   - min_level (INTEGER, DEFAULT 0)
   - created_at, updated_at timestamps
   - UNIQUE constraint on (product_id, location_id)

6. Purchase Orders
   - id (Primary Key)
   - supplier_id (Foreign Key to Suppliers)
   - order_date (DATE)
   - expected_delivery (DATE)
   - status (VARCHAR: 'pending', 'ordered', 'received', 'cancelled')
   - total_amount (DECIMAL)
   - notes (TEXT)
   - created_at, updated_at timestamps

7. Purchase Order Items
   - id (Primary Key)
   - purchase_order_id (Foreign Key to Purchase Orders)
   - product_id (Foreign Key to Products)
   - quantity (INTEGER)
   - unit_price (DECIMAL)
   - total_price (DECIMAL)
   - created_at, updated_at timestamps

8. Stock Alerts
   - id (Primary Key)
   - product_id (Foreign Key to Products)
   - location_id (Foreign Key to Locations)
   - alert_type (VARCHAR: 'low_stock', 'out_of_stock')
   - severity (VARCHAR: 'low', 'medium', 'high')
   - message (TEXT)
   - is_resolved (BOOLEAN, DEFAULT FALSE)
   - resolved_at (TIMESTAMP)
   - resolved_by (VARCHAR)
   - created_at, updated_at timestamps

Include proper foreign key relationships, indexes, and constraints.
```

### 3. API Endpoints Design
```
Create RESTful API endpoints for the inventory management system:

Products:
- GET /api/v1/products - List all products (with optional filters)
- GET /api/v1/products/{id} - Get product by ID
- POST /api/v1/products - Create new product
- PUT /api/v1/products/{id} - Update product
- DELETE /api/v1/products/{id} - Delete product

Categories:
- GET /api/v1/categories - List all categories
- GET /api/v1/categories/{id} - Get category by ID
- POST /api/v1/categories - Create new category
- PUT /api/v1/categories/{id} - Update category
- DELETE /api/v1/categories/{id} - Delete category

Suppliers:
- GET /api/v1/suppliers - List all suppliers
- GET /api/v1/suppliers/{id} - Get supplier by ID
- POST /api/v1/suppliers - Create new supplier
- PUT /api/v1/suppliers/{id} - Update supplier
- DELETE /api/v1/suppliers/{id} - Delete supplier

Locations:
- GET /api/v1/locations - List all locations
- GET /api/v1/locations/{id} - Get location by ID
- POST /api/v1/locations - Create new location
- PUT /api/v1/locations/{id} - Update location
- DELETE /api/v1/locations/{id} - Delete location

Inventory:
- GET /api/v1/inventory - List all inventory items (with optional filters)
- GET /api/v1/inventory/{id} - Get inventory item by ID
- POST /api/v1/inventory - Create new inventory item
- PUT /api/v1/inventory/{id} - Update inventory item
- DELETE /api/v1/inventory/{id} - Delete inventory item
- POST /api/v1/inventory/{id}/adjust - Adjust inventory quantity

Purchase Orders:
- GET /api/v1/purchase-orders - List all purchase orders (with optional filters)
- GET /api/v1/purchase-orders/{id} - Get purchase order by ID
- POST /api/v1/purchase-orders - Create new purchase order
- PUT /api/v1/purchase-orders/{id} - Update purchase order
- DELETE /api/v1/purchase-orders/{id} - Delete purchase order

Stock Alerts:
- GET /api/v1/stock-alerts - List all stock alerts (with optional filters)
- GET /api/v1/stock-alerts/{id} - Get stock alert by ID
- POST /api/v1/stock-alerts - Create new stock alert
- PUT /api/v1/stock-alerts/{id} - Update stock alert
- DELETE /api/v1/stock-alerts/{id} - Delete stock alert

Additional endpoints:
- GET /api/v1/dashboard/summary - Get dashboard summary data
- GET /api/v1/inventory/summary - Get inventory summary
- GET /health - Health check endpoint

Include proper error handling, validation, and response schemas.
```

## Backend Development Prompts

### 4. FastAPI Application Structure
```
Create a FastAPI application with the following structure:

1. Main application file (main.py):
   - FastAPI app initialization
   - CORS middleware configuration
   - API router inclusion
   - Health check endpoints
   - Startup and shutdown events

2. Configuration (app/core/config.py):
   - Settings class using Pydantic
   - Environment variable management
   - Database URL configuration
   - CORS origins configuration
   - Security settings

3. Database configuration (app/core/database.py):
   - SQLAlchemy engine setup
   - Session management
   - Base model class
   - Database connection utilities

4. API router structure (app/api/api_v1/api.py):
   - Main API router
   - Include all endpoint routers
   - API versioning

5. Endpoint modules (app/api/api_v1/endpoints/):
   - Separate router for each entity
   - CRUD operations
   - Proper error handling
   - Input validation

6. Models (app/models/):
   - SQLAlchemy model classes
   - Relationships between models
   - Timestamps and audit fields

7. Schemas (app/schemas/):
   - Pydantic models for request/response
   - Validation rules
   - Optional fields for updates

Include proper imports, error handling, and documentation.
```

### 5. Database Models Implementation
```
Create SQLAlchemy models for the inventory management system:

1. Base Model (app/models/base.py):
   - Abstract base class
   - Common fields (id, created_at, updated_at)
   - Timestamp management

2. Category Model (app/models/category.py):
   - id, name, description fields
   - Relationship to products
   - Proper constraints and indexes

3. Supplier Model (app/models/supplier.py):
   - id, name, email, phone, address, contact_person fields
   - Relationship to products and purchase orders
   - Email validation

4. Location Model (app/models/location.py):
   - id, name, address, description fields
   - Relationship to inventory items
   - Proper constraints

5. Product Model (app/models/product.py):
   - id, name, description, sku, price, cost fields
   - Foreign keys to category and supplier
   - Unique SKU constraint
   - Relationships to inventory and purchase order items

6. Inventory Model (app/models/inventory.py):
   - id, product_id, location_id, quantity, min_level fields
   - Foreign keys to product and location
   - Unique constraint on (product_id, location_id)
   - Relationships to product and location

7. Purchase Order Model (app/models/purchase_order.py):
   - id, supplier_id, order_date, expected_delivery, status fields
   - Foreign key to supplier
   - Status enum values
   - Relationship to items

8. Purchase Order Item Model (app/models/purchase_order_item.py):
   - id, purchase_order_id, product_id, quantity, unit_price fields
   - Foreign keys to purchase order and product
   - Calculated total_price field

9. Stock Alert Model (app/models/stock_alert.py):
   - id, product_id, location_id, alert_type, severity fields
   - Foreign keys to product and location
   - Resolution tracking fields

Include proper relationships, constraints, and indexes.
```

### 6. Pydantic Schemas Implementation
```
Create Pydantic schemas for the inventory management system:

1. Base schemas with common patterns:
   - BaseModel inheritance
   - Config classes for ORM mode
   - Common field types and validation

2. Category schemas:
   - CategoryBase: name, description
   - CategoryCreate: inherits from CategoryBase
   - CategoryUpdate: all fields optional
   - Category: includes id, timestamps

3. Supplier schemas:
   - SupplierBase: name, email, phone, address, contact_person
   - SupplierCreate: inherits from SupplierBase
   - SupplierUpdate: all fields optional
   - Supplier: includes id, timestamps

4. Location schemas:
   - LocationBase: name, address, description
   - LocationCreate: inherits from LocationBase
   - LocationUpdate: all fields optional
   - Location: includes id, timestamps

5. Product schemas:
   - ProductBase: name, description, sku, price, cost, category_id, supplier_id, is_active
   - ProductCreate: inherits from ProductBase
   - ProductUpdate: all fields optional
   - Product: includes id, timestamps, relationships

6. Inventory schemas:
   - InventoryBase: product_id, location_id, quantity, min_level
   - InventoryCreate: inherits from InventoryBase
   - InventoryUpdate: all fields optional
   - Inventory: includes id, timestamps, relationships

7. Purchase Order schemas:
   - PurchaseOrderBase: supplier_id, order_date, expected_delivery, status, total_amount, notes
   - PurchaseOrderCreate: inherits from PurchaseOrderBase
   - PurchaseOrderUpdate: all fields optional
   - PurchaseOrder: includes id, timestamps, relationships

8. Stock Alert schemas:
   - StockAlertBase: product_id, location_id, alert_type, severity, message
   - StockAlertCreate: inherits from StockAlertBase
   - StockAlertUpdate: all fields optional
   - StockAlert: includes id, timestamps, resolution fields

Include proper validation rules, field types, and relationships.
```

## Frontend Development Prompts

### 7. React Application Structure
```
Create a React application with TypeScript for the inventory management system:

1. Project structure:
   - src/components/: Reusable UI components
   - src/pages/: Page components for each feature
   - src/services/: API service functions
   - src/types/: TypeScript type definitions
   - src/utils/: Utility functions
   - src/hooks/: Custom React hooks

2. Main App component:
   - React Router setup
   - Navigation structure
   - Layout components
   - Error boundaries

3. Navigation component:
   - Responsive navigation bar
   - Active route highlighting
   - Dropdown menus for settings
   - Mobile menu support

4. Dashboard page:
   - Summary cards for key metrics
   - Charts and graphs
   - Recent activity feed
   - Quick action buttons

5. CRUD pages for each entity:
   - List view with search and filters
   - Create/Edit forms
   - Delete confirmation dialogs
   - Loading and error states

6. Form components:
   - Reusable form components
   - Validation handling
   - Error message display
   - Success feedback

Include proper TypeScript types, error handling, and responsive design.
```

### 8. API Service Implementation
```
Create API service functions for the React frontend:

1. Base API configuration:
   - Axios instance setup
   - Base URL configuration
   - Request/response interceptors
   - Error handling
   - Authentication headers

2. Products API:
   - getAll(): Get all products with optional filters
   - getById(id): Get product by ID
   - create(product): Create new product
   - update(id, product): Update product
   - delete(id): Delete product

3. Categories API:
   - getAll(): Get all categories
   - getById(id): Get category by ID
   - create(category): Create new category
   - update(id, category): Update category
   - delete(id): Delete category

4. Suppliers API:
   - getAll(): Get all suppliers
   - getById(id): Get supplier by ID
   - create(supplier): Create new supplier
   - update(id, supplier): Update supplier
   - delete(id): Delete supplier

5. Locations API:
   - getAll(): Get all locations
   - getById(id): Get location by ID
   - create(location): Create new location
   - update(id, location): Update location
   - delete(id): Delete location

6. Inventory API:
   - getAll(): Get all inventory items with optional filters
   - getById(id): Get inventory item by ID
   - create(inventory): Create new inventory item
   - update(id, inventory): Update inventory item
   - delete(id): Delete inventory item
   - adjust(id, adjustment): Adjust inventory quantity

7. Purchase Orders API:
   - getAll(): Get all purchase orders with optional filters
   - getById(id): Get purchase order by ID
   - create(purchaseOrder): Create new purchase order
   - update(id, purchaseOrder): Update purchase order
   - delete(id): Delete purchase order

8. Stock Alerts API:
   - getAll(): Get all stock alerts with optional filters
   - getById(id): Get stock alert by ID
   - create(stockAlert): Create new stock alert
   - update(id, stockAlert): Update stock alert
   - delete(id): Delete stock alert

Include proper TypeScript types, error handling, and loading states.
```

### 9. TypeScript Types Definition
```
Create TypeScript type definitions for the inventory management system:

1. Base types:
   - Common interface patterns
   - API response types
   - Error types
   - Loading states

2. Category types:
   - Category interface
   - CategoryCreate interface
   - CategoryUpdate interface

3. Supplier types:
   - Supplier interface
   - SupplierCreate interface
   - SupplierUpdate interface

4. Location types:
   - Location interface
   - LocationCreate interface
   - LocationUpdate interface

5. Product types:
   - Product interface
   - ProductCreate interface
   - ProductUpdate interface
   - Product filters interface

6. Inventory types:
   - InventoryItem interface
   - InventoryItemCreate interface
   - InventoryItemUpdate interface
   - InventoryAdjustment interface

7. Purchase Order types:
   - PurchaseOrder interface
   - PurchaseOrderCreate interface
   - PurchaseOrderUpdate interface
   - PurchaseOrderItem interface

8. Stock Alert types:
   - StockAlert interface
   - StockAlertCreate interface
   - StockAlertUpdate interface

9. Dashboard types:
   - DashboardSummary interface
   - InventorySummary interface
   - Chart data types

10. API types:
    - API response wrapper
    - Pagination types
    - Filter types
    - Error response types

Include proper optional fields, union types, and generic types where appropriate.
```

## Deployment Prompts

### 10. Railway Deployment Configuration
```
Configure Railway deployment for the inventory management system:

1. Backend deployment:
   - Dockerfile configuration
   - Environment variables setup
   - Database connection configuration
   - Health check endpoints
   - Migration scripts

2. Frontend deployment:
   - Build configuration
   - Environment variables for API URL
   - Static file serving
   - CORS configuration

3. Database setup:
   - Railway PostgreSQL provisioning
   - Connection string configuration
   - Migration execution
   - Initial data seeding

4. Environment variables:
   - DATABASE_URL: PostgreSQL connection string
   - SECRET_KEY: Application secret key
   - PORT: Port number
   - REACT_APP_API_URL: Frontend API URL
   - NODE_ENV: Environment mode

5. Health checks:
   - API health endpoint
   - Database connection check
   - Frontend availability check

6. Monitoring:
   - Log aggregation
   - Error tracking
   - Performance monitoring

Include proper error handling, logging, and monitoring.
```

### 11. Docker Configuration
```
Create Docker configuration for the inventory management system:

1. Backend Dockerfile:
   - Python 3.11 base image
   - Dependencies installation
   - Application code copying
   - Port exposure
   - Entry point script

2. Frontend Dockerfile:
   - Node.js base image
   - Dependencies installation
   - Build process
   - Nginx configuration
   - Static file serving

3. Docker Compose configuration:
   - Backend service
   - Frontend service
   - Database service
   - Network configuration
   - Volume mounts

4. Entry point scripts:
   - Database migration execution
   - Application startup
   - Health check implementation
   - Error handling

5. Environment configuration:
   - Development environment
   - Production environment
   - Environment-specific settings

Include proper security practices, optimization, and best practices.
```

## Testing Prompts

### 12. Backend Testing
```
Create comprehensive testing for the backend API:

1. Unit tests:
   - Model validation tests
   - Schema validation tests
   - Utility function tests
   - Database operation tests

2. Integration tests:
   - API endpoint tests
   - Database integration tests
   - Authentication tests
   - Error handling tests

3. Test configuration:
   - Test database setup
   - Test fixtures
   - Mock services
   - Test utilities

4. Test coverage:
   - API endpoints coverage
   - Business logic coverage
   - Error scenarios coverage
   - Edge cases coverage

Include proper test organization, fixtures, and assertions.
```

### 13. Frontend Testing
```
Create comprehensive testing for the React frontend:

1. Unit tests:
   - Component tests
   - Hook tests
   - Utility function tests
   - Service function tests

2. Integration tests:
   - API integration tests
   - User interaction tests
   - Form validation tests
   - Navigation tests

3. E2E tests:
   - User workflow tests
   - Critical path tests
   - Cross-browser tests
   - Performance tests

4. Test configuration:
   - Testing library setup
   - Mock API responses
   - Test utilities
   - Coverage reporting

Include proper test organization, mocking, and assertions.
```

## Security Prompts

### 14. Security Implementation
```
Implement security measures for the inventory management system:

1. Authentication:
   - JWT token implementation
   - User management
   - Password hashing
   - Session management

2. Authorization:
   - Role-based access control
   - Permission system
   - API endpoint protection
   - Resource-level access control

3. Input validation:
   - Request validation
   - SQL injection prevention
   - XSS protection
   - CSRF protection

4. Data protection:
   - Sensitive data encryption
   - Audit logging
   - Data backup
   - Privacy compliance

5. API security:
   - Rate limiting
   - Request throttling
   - API key management
   - CORS configuration

Include proper security best practices and compliance measures.
```

## Performance Prompts

### 15. Performance Optimization
```
Implement performance optimizations for the inventory management system:

1. Backend optimization:
   - Database query optimization
   - Connection pooling
   - Caching strategies
   - API response optimization

2. Frontend optimization:
   - Code splitting
   - Lazy loading
   - Bundle optimization
   - Image optimization

3. Database optimization:
   - Index optimization
   - Query optimization
   - Partitioning strategies
   - Maintenance procedures

4. Caching strategies:
   - Redis caching
   - CDN configuration
   - Browser caching
   - API response caching

Include proper monitoring, profiling, and optimization techniques.
```

## Conclusion

These development prompts provide a comprehensive guide for building and maintaining the Inventory Management System. They cover all aspects of development from initial setup to deployment and optimization.

The prompts can be used as a reference for:
- New feature development
- Bug fixes and improvements
- System maintenance
- Team onboarding
- Code reviews

Each prompt includes specific requirements, implementation details, and best practices to ensure high-quality, maintainable code.

---

**Last Updated**: August 12, 2025  
**Version**: 1.0.0  
**Status**: Production Ready
