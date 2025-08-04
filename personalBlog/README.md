# Personal Blog

A modern, minimalist personal blog built with FastAPI and featuring a beautiful markdown editor for content creation.

![Blog Preview](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## ✨ Features

### 🎨 **Modern UI/UX**

- Clean, responsive design with Bootstrap 5
- Beautiful gradient navbar and smooth animations
- Mobile-friendly layout
- Dark code syntax highlighting

### ✍️ **Rich Content Creation**

- **SimpleMDE Markdown Editor** with live preview
- Auto-save functionality (localStorage)
- Markdown syntax highlighting and toolbar
- Quick reference guide for markdown

### 🔐 **Admin Features**

- Secure JWT-based authentication
- Admin-only content management
- Create, edit, and delete articles
- Protected routes with proper authorization

### 📝 **Article Management**

- Markdown-to-HTML rendering
- Publication date tracking
- Article listing with previews
- Share functionality (WhatsApp, Twitter, Copy Link)

### 🚀 **Performance & SEO**

- Fast loading with minimal dependencies
- Clean URLs and proper meta tags
- Optimized database queries
- CDN-based assets

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.13+)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5 + Vanilla JavaScript
- **Authentication**: JWT with Argon2 password hashing
- **Migrations**: Alembic
- **Editor**: SimpleMDE Markdown Editor
- **Styling**: Custom CSS with Font Awesome icons

## 📦 Installation

### Prerequisites

- Python 3.13+
- uv (recommended) or pip

### 1. Clone the Repository

```bash
git clone <repository-url>
cd personalBlog
```

### 2. Set up Virtual Environment

```bash
# Using uv (recommended)
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
DATABASE_URL=sqlite:///./personalBlog.db
```

### 4. Database Setup

```bash
# Run database migrations
alembic upgrade head

# Create default admin user
python scripts/create_default_admin.py
```

### 5. Run the Application

```bash
# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn app.main:app --reload
```

The blog will be available at `http://localhost:8000`

## 🚀 Quick Start

### Default Admin Credentials

After running the admin creation script:

- **Email**: `admin@example.com`
- **Username**: `admin`
- **Password**: `password`

**⚠️ Important**: Change these credentials after first login!

### Creating Your First Article

1. Navigate to `http://localhost:8000`
2. Click "Admin Sign In" and login with default credentials
3. Click "Add New Article" button
4. Write your content using the markdown editor
5. Click "Publish Article"

## 📁 Project Structure

```
personalBlog/
├── app/
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── article.py         # Article CRUD operations
│   │   └── auth.py            # Authentication routes
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── article.py         # Article model
│   │   ├── auth.py            # User model
│   │   └── base.py            # Base model
│   ├── templates/             # Jinja2 HTML templates
│   │   ├── base.html          # Base template
│   │   ├── index.html         # Home page
│   │   ├── login.html         # Login page
│   │   ├── article.html       # Article view
│   │   ├── new_article.html   # Create article
│   │   ├── edit_article.html  # Edit article
│   │   └── templates.py       # Template configuration
│   ├── auth_utils.py          # Authentication utilities
│   ├── db.py                  # Database configuration
│   ├── main.py                # FastAPI application
│   ├── schemas.py             # Pydantic models
│   └── utils.py               # Utility functions
├── alembic/                   # Database migrations
├── scripts/
│   └── create_default_admin.py # Admin user creation
├── .env                       # Environment variables
├── alembic.ini               # Alembic configuration
├── pyproject.toml            # Project dependencies
└── README.md
```

## 🎯 Usage

### Public Features

- **Home Page**: Browse all published articles
- **Article Reading**: View full articles with rendered markdown
- **Responsive Design**: Works on desktop, tablet, and mobile

### Admin Features (Login Required)

- **Article Management**: Create, edit, delete articles
- **Rich Editor**: SimpleMDE with live preview and auto-save
- **Content Control**: Full CRUD operations on articles

## 🔧 Configuration

### Environment Variables

| Variable                      | Description         | Default                       |
| ----------------------------- | ------------------- | ----------------------------- |
| `SECRET_KEY`                  | JWT signing secret  | Required                      |
| `ALGORITHM`                   | JWT algorithm       | `HS256`                       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration    | `15`                          |
| `DATABASE_URL`                | Database connection | `sqlite:///./personalBlog.db` |

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🚦 API Endpoints

### Public Routes

- `GET /` - Home page with article list
- `GET /article/{id}` - View specific article
- `GET /auth/login` - Login page

### Protected Routes (Admin Only)

- `GET /article/new` - New article form
- `POST /article/new_article` - Create article
- `GET /article/edit/{id}` - Edit article form
- `PUT /article/edit/{id}` - Update article
- `DELETE /article/{id}` - Delete article
- `POST /auth/login` - Authenticate user
- `GET /auth/logout` - Logout user

## 🎨 Customization

### Styling

- Modify `app/templates/base.html` for global styles
- Color scheme uses CSS custom properties
- Bootstrap classes for responsive design

### Content

- Update navbar title in `base.html`
- Customize footer content
- Add your own logo/branding

### Features

- Add categories/tags to articles
- Implement comment system
- Add search functionality
- Configure email notifications

## 🔒 Security Features

- **Password Hashing**: Argon2 for secure password storage
- **JWT Authentication**: Secure token-based auth
- **CSRF Protection**: Built-in FastAPI security
- **Input Validation**: Pydantic schema validation
- **SQL Injection Protection**: SQLAlchemy ORM

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**

```bash
# Ensure database file exists and permissions are correct
ls -la personalBlog.db
```

**SimpleMDE Not Loading**

- Check internet connection (CDN dependencies)
- Verify browser console for JavaScript errors

**Authentication Issues**

- Clear browser cookies
- Check JWT secret key configuration
- Verify token expiration settings

### Development

```bash
# Enable debug mode
uvicorn app.main:app --reload --log-level debug

# Check database content
sqlite3 personalBlog.db
.tables
SELECT * FROM users;
SELECT * FROM articles;
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [SimpleMDE](https://github.com/sparksuite/simplemde-markdown-editor) - Markdown editor
- [Font Awesome](https://fontawesome.com/) - Icons
- [SQLAlchemy](https://sqlalchemy.org/) - Database ORM

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information

---

**Happy Blogging!** 🎉
