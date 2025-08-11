# Complete Development Documentation - Inventory Management System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Backend Development](#backend-development)
6. [Frontend Development](#frontend-development)
7. [Database Design](#database-design)
8. [API Documentation](#api-documentation)
9. [Deployment](#deployment)
10. [Development Setup](#development-setup)

## Project Overview

The Inventory Management System is a comprehensive web application designed to manage inventory, products, suppliers, locations, purchase orders, and stock alerts. It provides a modern, responsive interface with a robust backend API.

### Key Features
- **Product Management**: CRUD operations for products with categories and suppliers
- **Inventory Tracking**: Real-time inventory levels across multiple locations
- **Supplier Management**: Complete supplier information and contact details
- **Purchase Orders**: Create and manage purchase orders with items
- **Stock Alerts**: Automated alerts for low stock and out-of-stock items
- **Location Management**: Multi-location inventory support
- **Dashboard**: Real-time overview of inventory status

## Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
│                 │    │                 │    │                 │
│ - Dashboard     │    │ - REST API      │    │ - Tables        │
│ - Forms         │    │ - Authentication │   │ - Relationships │
│ - Components    │    │ - Validation     │    │ - Indexes       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Authentication**: JWT tokens
- **Documentation**: OpenAPI/Swagger

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Build Tool**: Vite

### DevOps & Deployment
- **Containerization**: Docker
- **Cloud Platform**: Railway
- **Database**: Railway PostgreSQL
- **Version Control**: Git

## Project Structure

```
inventory-management/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── api_v1/
│   │   │       ├── endpoints/
│   │   │       └── api.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── utils/
│   ├── alembic/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── public/
│   └── package.json
├── documents/
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Backend Development

### FastAPI Application Structure

#### Main Application (`main.py`)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(
    title="Inventory Management API",
    description="A comprehensive inventory management system API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
```

#### Configuration (`app/core/config.py`)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Inventory Management API"
    DATABASE_URL: str = ""
    SECRET_KEY: str = "your-secret-key-change-in-production"
    BACKEND_CORS_ORIGINS: list = ["*"]
    DEBUG: bool = True
    PORT: int = 8000
```

#### Database Configuration (`app/core/database.py`)
```python
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### API Endpoints Structure

#### Products API (`app/api/api_v1/endpoints/products.py`)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, Product
from app.models.product import Product as ProductModel

router = APIRouter()

@router.get("/", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
```

## Frontend Development

### React Application Structure

#### Main App Component (`src/App.tsx`)
```typescript
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/products" element={<Products />} />
            <Route path="/inventory" element={<Inventory />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
```

#### API Service (`src/services/api.ts`)
```typescript
import axios from 'axios';

const getApiBaseUrl = () => {
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  if (process.env.NODE_ENV === 'production') {
    return 'https://inventory-management-production-82d5.up.railway.app';
  }
  
  return 'http://localhost:8000';
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  maxRedirects: 5,
  timeout: 10000,
});

export const productsApi = {
  getAll: async (): Promise<Product[]> => {
    const response = await api.get('/products');
    return response.data;
  },
  
  create: async (product: ProductCreate): Promise<Product> => {
    const response = await api.post('/products', product);
    return response.data;
  },
};
```

## Database Design

### Entity Relationship Diagram

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Categories  │    │ Products    │    │ Suppliers   │
│             │    │             │    │             │
│ id (PK)     │◄───┤ category_id │    │ id (PK)     │
│ name        │    │ supplier_id ├────┤ name        │
│ description │    │ name        │    │ email       │
└─────────────┘    │ sku         │    │ phone       │
                   │ price       │    └─────────────┘
                   │ cost        │
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Inventory   │
                   │             │
                   │ product_id  │
                   │ location_id │
                   │ quantity    │
                   │ min_level   │
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Locations   │
                   │             │
                   │ id (PK)     │
                   │ name        │
                   │ address     │
                   └─────────────┘
```

### Database Tables

#### Categories Table
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    sku VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    supplier_id INTEGER REFERENCES suppliers(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Documentation

### Base URL
```
Production: https://inventory-management-production-82d5.up.railway.app/api/v1
Development: http://localhost:8000/api/v1
```

### Endpoints

#### Products
- `GET /products` - Get all products
- `GET /products/{id}` - Get product by ID
- `POST /products` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

#### Categories
- `GET /categories` - Get all categories
- `GET /categories/{id}` - Get category by ID
- `POST /categories` - Create new category
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

#### Suppliers
- `GET /suppliers` - Get all suppliers
- `GET /suppliers/{id}` - Get supplier by ID
- `POST /suppliers` - Create new supplier
- `PUT /suppliers/{id}` - Update supplier
- `DELETE /suppliers/{id}` - Delete supplier

#### Inventory
- `GET /inventory` - Get all inventory items
- `GET /inventory/{id}` - Get inventory item by ID
- `POST /inventory` - Create new inventory item
- `PUT /inventory/{id}` - Update inventory item
- `DELETE /inventory/{id}` - Delete inventory item

## Deployment

### Railway Deployment

#### Backend Deployment
1. **Create Railway Project**
   ```bash
   railway login
   railway init
   ```

2. **Configure Environment Variables**
   - `DATABASE_URL`: Railway PostgreSQL connection string
   - `SECRET_KEY`: Application secret key
   - `PORT`: Port number (Railway sets this automatically)

3. **Deploy**
   ```bash
   railway up
   ```

#### Frontend Deployment
1. **Build the Application**
   ```bash
   cd frontend
   npm run build
   ```

2. **Deploy to Railway**
   ```bash
   railway up
   ```

### Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY entrypoint.sh ./

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["./entrypoint.sh"]
```

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

### Backend Setup
```bash
# Clone repository
git clone <repository-url>
cd inventory-management

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
cd backend
alembic upgrade head

# Start development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

### Database Setup
```bash
# Create database
createdb inventory_management

# Run migrations
cd backend
alembic upgrade head

# Seed data (optional)
python seed_data.py
```

---

**Last Updated**: August 12, 2025  
**Version**: 1.0.0  
**Status**: Production Ready
