# Inventory Management System

A full-stack inventory management system built with React frontend, Python FastAPI backend, and PostgreSQL database.

## 🏗️ Architecture

- **Frontend**: React 18 with TypeScript, TailwindCSS, React Router
- **Backend**: Python FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **API Documentation**: Swagger UI (FastAPI)

## 📁 Project Structure

```
inventory-management/
├── frontend/                 # React frontend application
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API service functions
│   │   ├── types/          # TypeScript type definitions
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── tailwind.config.js
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── main.py
├── database/               # Database migrations and scripts
│   └── init.sql
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile.frontend     # Frontend Dockerfile
├── Dockerfile.backend      # Backend Dockerfile
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd inventory-management
   ```

2. **Start all services**
   ```bash
   docker-compose up -d
   ```

3. **Access the applications**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database: localhost:5432

### Local Development

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run the backend**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

## 📚 API Documentation

Once the backend is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core API Endpoints

- `GET /api/health` - Health check
- `GET /api/items` - List all inventory items
- `POST /api/items` - Create new inventory item
- `GET /api/items/{id}` - Get specific item
- `PUT /api/items/{id}` - Update item
- `DELETE /api/items/{id}` - Delete item

## 🛠️ Development

### Backend Development

The backend follows a clean architecture pattern:
- **Models**: SQLAlchemy ORM models
- **Schemas**: Pydantic models for request/response validation
- **Services**: Business logic layer
- **API Routes**: FastAPI route handlers

### Frontend Development

The frontend uses:
- **React Router**: For navigation
- **TailwindCSS**: For styling
- **TypeScript**: For type safety
- **Axios**: For API communication

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild services
docker-compose up -d --build

# Access database
docker-compose exec db psql -U postgres -d inventory
```

## 🔧 Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/inventory
SECRET_KEY=your-secret-key
DEBUG=True
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## 📝 Features

- [x] CRUD operations for inventory items
- [x] Responsive web interface
- [x] RESTful API
- [x] Database persistence
- [x] Docker containerization
- [x] API documentation
- [x] Type safety (TypeScript)
- [x] Modern UI with TailwindCSS

## 🚧 Roadmap

- [ ] User authentication and authorization
- [ ] Role-based access control
- [ ] Inventory categories and tags
- [ ] Stock alerts and notifications
- [ ] Barcode scanning
- [ ] Export/import functionality
- [ ] Analytics and reporting
- [ ] Mobile responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.
