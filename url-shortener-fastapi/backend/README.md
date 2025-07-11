# URL Shortener FastAPI

A modern, fast, and secure URL shortener service built with FastAPI and SQLAlchemy. This application allows users to create shortened URLs with custom expiration times, track click statistics, and manage their URLs through a RESTful API.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **URL Shortening**: Create short URLs with custom expiration times
- **Click Tracking**: Track clicks and visitor statistics for each shortened URL
- **User Management**: Each user has their own URL collection with configurable TTL limits
- **Database Migrations**: Alembic for database schema management
- **CORS Support**: Cross-origin resource sharing enabled for web applications
- **Security**: Password hashing with bcrypt and JWT token authentication

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Primary database (configurable)
- **JWT**: JSON Web Tokens for authentication
- **Passlib**: Password hashing library
- **Pydantic**: Data validation and serialization

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py          # Authentication endpoints
│   │   └── url.py           # URL shortening endpoints
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── url.py           # URL model
│   │   └── url_visits.py    # URL visit tracking model
│   ├── auth_utils.py        # JWT and password utilities
│   ├── db.py               # Database configuration
│   ├── main.py             # FastAPI application entry point
│   ├── schemas.py          # Pydantic models for request/response
│   └── utils.py            # Utility functions
├── alembic/                # Database migrations
├── requirements.txt        # Python dependencies
└── pyproject.toml         # Project configuration
```

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL (or SQLite for development)
- pip or uv package manager

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd url-shortener-fastapi/backend
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
# Or if using uv:
uv sync
```

4. Set up environment variables:
   Create a `.env` file in the backend directory:

```env
DATABASE_URL=postgresql://username:password@localhost/url_shortener
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run database migrations:

```bash
alembic upgrade head
```

6. Start the application:

```bash
python app/main.py
# Or using uvicorn directly:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:

- **Interactive API docs (Swagger UI)**: `http://localhost:8000/docs`
- **Alternative API docs (ReDoc)**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /user/register` - Register a new user
- `POST /user/login` - Login and get access token
- `GET /user/me` - Get current user information
- `GET /user/refresh_token` - Refresh access token

### URL Management

- `POST /urls/shorten` - Create a shortened URL
- `GET /urls/get_user_urls` - Get all URLs for the current user
- `GET /urls/{short_code}` - Redirect to original URL (public endpoint)
- `DELETE /urls/{short_code}` - Delete a shortened URL
- `GET /urls/stats/{short_code}` - Get click statistics for a URL

## Usage Examples

### Register a new user

```bash
curl -X POST "http://localhost:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword"
  }'
```

### Create a shortened URL

```bash
curl -X POST "http://localhost:8000/urls/shorten" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "original_url": "https://example.com/very-long-url",
    "ttl_minutes": 60
  }'
```

### Access a shortened URL

```bash
curl -L "http://localhost:8000/urls/{short_code}"
```

## Database Schema

### Users Table

- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `password`: Hashed password
- `max_ttl_minutes`: Maximum TTL allowed for user's URLs (default: 60 minutes)
- `created_at`, `updated_at`: Timestamps

### URLs Table

- `id`: Primary key
- `original_url`: The original long URL
- `short_url`: The generated short code
- `click_count`: Number of times the URL has been accessed
- `last_visited`: Timestamp of last access
- `expires_at`: Expiration timestamp
- `user_id`: Foreign key to users table
- `created_at`, `updated_at`: Timestamps

### URL Visits Table

- Tracks detailed visitor information for analytics
- Links to URLs table for visit tracking

## Configuration

The application can be configured through environment variables:

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: JWT signing secret
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Development

### Running Tests

```bash
# Add your test commands here
pytest
```

### Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

Rollback migration:

```bash
alembic downgrade -1
```

### Code Quality

The project uses:

- Ruff for linting and formatting
- Type hints for better code quality
- Pydantic for data validation

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- CORS configuration for web security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the GitHub repository or contact the development team.
