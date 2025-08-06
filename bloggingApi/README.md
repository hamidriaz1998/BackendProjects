# Blogging API

A complete REST API for a blogging platform built with FastAPI, SQLAlchemy, and SQLite. This API provides full CRUD operations for managing posts, categories, and tags with proper relationships and validation.

## Features

- **Posts Management**: Create, read, update, and delete blog posts
- **Categories Management**: Organize posts into categories
- **Tags Management**: Add multiple tags to posts for better organization
- **Relationships**: Many-to-many relationship between posts and tags, one-to-many between categories and posts
- **Validation**: Input validation and error handling
- **Auto Documentation**: Interactive API documentation with Swagger UI
- **Pagination**: Support for paginated results

## Project Structure

```
bloggingApi/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── posts.py          # Posts endpoints
│   │   ├── categories.py     # Categories endpoints
│   │   └── tags.py           # Tags endpoints
│   ├── __init__.py
│   ├── main.py               # FastAPI application
│   ├── models.py             # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   ├── db.py                 # Database configuration
│   └── test.py
├── migrations/               # Alembic migrations
├── test_api.py              # API testing script
├── pyproject.toml           # Project dependencies
└── README.md
```

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd bloggingApi
   ```

2. **Install dependencies using uv**

   ```bash
   uv sync
   ```

3. **Activate virtual environment**
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

## Running the API

1. **Start the server**

   ```bash
   python -m app.main
   ```

2. **Alternative using uvicorn directly**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**
   - API Base URL: `http://localhost:8000`
   - Interactive Documentation: `http://localhost:8000/docs`
   - Alternative Documentation: `http://localhost:8000/redoc`

## API Endpoints

### Root & Health

| Method | Endpoint  | Description                             |
| ------ | --------- | --------------------------------------- |
| GET    | `/`       | API information and available endpoints |
| GET    | `/health` | Health check endpoint                   |

### Posts

| Method | Endpoint                        | Description                     |
| ------ | ------------------------------- | ------------------------------- |
| GET    | `/posts/`                       | Get all posts (with pagination) |
| GET    | `/posts/{id}`                   | Get a specific post by ID       |
| POST   | `/posts/`                       | Create a new post               |
| PUT    | `/posts/{id}`                   | Update an existing post         |
| DELETE | `/posts/{id}`                   | Delete a post                   |
| GET    | `/posts/category/{category_id}` | Get posts by category           |
| GET    | `/posts/tag/{tag_id}`           | Get posts by tag                |

### Categories

| Method | Endpoint           | Description                          |
| ------ | ------------------ | ------------------------------------ |
| GET    | `/categories/`     | Get all categories (with pagination) |
| GET    | `/categories/{id}` | Get a specific category by ID        |
| POST   | `/categories/`     | Create a new category                |
| PUT    | `/categories/{id}` | Update an existing category          |
| DELETE | `/categories/{id}` | Delete a category                    |

### Tags

| Method | Endpoint     | Description                    |
| ------ | ------------ | ------------------------------ |
| GET    | `/tags/`     | Get all tags (with pagination) |
| GET    | `/tags/{id}` | Get a specific tag by ID       |
| POST   | `/tags/`     | Create a new tag               |
| PUT    | `/tags/{id}` | Update an existing tag         |
| DELETE | `/tags/{id}` | Delete a tag                   |

## Request/Response Examples

### Create a Post

```bash
curl -X POST "http://localhost:8000/posts/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Getting Started with FastAPI",
    "content": "FastAPI is a modern web framework...",
    "category": "Technology",
    "tags": ["python", "fastapi", "tutorial"]
  }'
```

**Response:**

```json
{
  "id": 1,
  "title": "Getting Started with FastAPI",
  "content": "FastAPI is a modern web framework...",
  "category": {
    "id": 1,
    "name": "Technology"
  },
  "tags": [
    { "id": 1, "name": "python" },
    { "id": 2, "name": "fastapi" },
    { "id": 3, "name": "tutorial" }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Create a Category

```bash
curl -X POST "http://localhost:8000/categories/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Technology"}'
```

### Create a Tag

```bash
curl -X POST "http://localhost:8000/tags/" \
  -H "Content-Type: application/json" \
  -d '{"name": "python"}'
```

### Update a Post

```bash
curl -X PUT "http://localhost:8000/posts/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Advanced FastAPI Tutorial",
    "content": "Updated content...",
    "tags": ["python", "fastapi", "advanced"]
  }'
```

### Get Posts with Pagination

```bash
curl "http://localhost:8000/posts/?skip=0&limit=10"
```

## Data Models

### Post Model

- `id`: Integer (Primary Key)
- `title`: String (Required, Unique)
- `content`: Text (Required)
- `category_id`: Integer (Foreign Key, Optional)
- `created_at`: DateTime (Auto-generated)
- `updated_at`: DateTime (Auto-updated)

### Category Model

- `id`: Integer (Primary Key)
- `name`: String (Required, Unique)

### Tag Model

- `id`: Integer (Primary Key)
- `name`: String (Required, Unique)

### Relationships

- **Post ↔ Category**: Many-to-One (A post can have one category, a category can have many posts)
- **Post ↔ Tag**: Many-to-Many (A post can have many tags, a tag can be used in many posts)

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200`: Success
- `400`: Bad Request (validation errors, duplicates)
- `404`: Not Found
- `422`: Unprocessable Entity (validation errors)

Example error response:

```json
{
  "detail": "Post not found"
}
```

## Testing

### Automated Testing

Run the included test script:

```bash
python test_api.py
```

This script tests:

- All CRUD operations for posts, categories, and tags
- Error handling
- Relationships between entities
- Pagination

### Manual Testing

Use the interactive documentation at `http://localhost:8000/docs` to test endpoints manually.

## Pagination

All list endpoints support pagination with query parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

Example:

```
GET /posts/?skip=10&limit=5
```

## Database

- **Database**: SQLite (`bloggingApi.db`)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic (configured but migrations in `migrations/` folder)

## Configuration

The database URL can be configured via environment variable:

```bash
export DATABASE_URL="sqlite:///bloggingApi.db"
```

## Development

### Adding New Features

1. **Models**: Add/modify models in `app/models.py`
2. **Schemas**: Add/modify Pydantic schemas in `app/schemas.py`
3. **Endpoints**: Add new endpoints in respective API files in `app/api/`
4. **Register Routes**: Import and register new routers in `app/main.py`

### Database Migrations

To create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Dependencies

- **FastAPI**: Modern web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server
- **Alembic**: Database migrations
- **python-dotenv**: Environment variables management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
