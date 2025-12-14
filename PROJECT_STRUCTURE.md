# Complete Project Structure

This document provides a complete overview of the project structure and all files.

## File Tree

```
kino/
├── backend/                          # Django backend application
│   ├── config/                       # Django project configuration
│   │   ├── __init__.py
│   │   ├── asgi.py                   # ASGI configuration
│   │   ├── settings.py               # Django settings with env vars
│   │   ├── urls.py                   # Main URL routing
│   │   └── wsgi.py                   # WSGI configuration
│   ├── movies/                       # Movies Django app
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── filters.py                # Custom filters (optional)
│   │   ├── models.py                 # Database models (Movie, Genre, Actor, Review)
│   │   ├── serializers.py            # DRF serializers
│   │   ├── tests.py                  # Unit tests
│   │   ├── views.py                  # API views and ViewSets
│   │   ├── migrations/               # Database migrations
│   │   │   └── __init__.py
│   │   ├── management/              # Custom management commands
│   │   │   ├── __init__.py
│   │   │   └── commands/
│   │   │       ├── __init__.py
│   │   │       ├── create_superuser.py    # Create superuser from env
│   │   │       └── import_sample_data.py  # Import sample movies
│   │   └── urls/                    # URL routing for movies app
│   │       ├── __init__.py
│   │       ├── api.py               # API endpoints
│   │       └── auth.py              # Authentication endpoints
│   ├── Dockerfile                   # Backend Docker image
│   ├── .dockerignore                # Docker ignore patterns
│   ├── manage.py                    # Django management script
│   └── requirements.txt             # Python dependencies
│
├── src/                             # React frontend application
│   ├── components/                  # Reusable React components
│   │   ├── Form.css                 # Form styles
│   │   ├── LoginForm.jsx            # Login form component
│   │   ├── MovieCard.css            # Movie card styles
│   │   ├── MovieCard.jsx            # Movie card component
│   │   ├── Navbar.css               # Navbar styles
│   │   ├── Navbar.jsx                # Navigation bar component
│   │   ├── Pagination.css           # Pagination styles
│   │   ├── Pagination.jsx           # Pagination component
│   │   └── RegisterForm.jsx         # Registration form component
│   ├── contexts/                    # React contexts
│   │   └── AuthContext.jsx          # Authentication context
│   ├── pages/                       # Page components
│   │   ├── AdminPanel.css           # Admin panel styles
│   │   ├── AdminPanel.jsx           # Admin panel page
│   │   ├── Home.css                 # Home page styles
│   │   ├── Home.jsx                 # Home page with movie list
│   │   ├── MovieDetail.css          # Movie detail styles
│   │   ├── MovieDetail.jsx          # Movie detail page
│   │   ├── Profile.css               # Profile page styles
│   │   └── Profile.jsx               # User profile page
│   ├── services/                    # API services
│   │   └── api.js                   # Axios API client
│   ├── App.css                      # Main app styles
│   ├── App.jsx                      # Main app component with routing
│   ├── index.css                    # Global styles
│   └── main.jsx                     # React entry point
│
├── .github/                         # GitHub Actions workflows
│   └── workflows/
│       └── docker-build.yml         # CI/CD workflow for Docker images
│
├── public/                          # Static public files
│   └── vite.svg
│
├── Dockerfile                       # Frontend Docker image (multi-stage)
├── .dockerignore                   # Frontend Docker ignore patterns
├── docker-compose.yml              # Development Docker Compose
├── docker-compose.prod.yml         # Production Docker Compose
├── nginx.conf                      # Nginx config for development
├── nginx.prod.conf                 # Nginx config for production
├── env.example                     # Environment variables example
├── .gitignore                      # Git ignore patterns
├── eslint.config.js                # ESLint configuration
├── index.html                      # HTML entry point
├── package.json                    # Node.js dependencies
├── package-lock.json               # Locked Node.js dependencies
├── vite.config.js                  # Vite configuration
└── README.md                       # Project documentation

```

## Key Files Summary

### Backend Files

1. **backend/config/settings.py** - Django settings with:
   - Environment variable configuration
   - PostgreSQL database setup
   - JWT authentication
   - CORS configuration
   - Media/static file handling
   - Security settings for production

2. **backend/movies/models.py** - Database models:
   - `Genre` - Movie genres
   - `Actor` - Movie actors
   - `Movie` - Main movie model with M2M relations
   - `Review` - User reviews with ratings

3. **backend/movies/views.py** - API endpoints:
   - `MovieViewSet` - CRUD operations, search, filter, sorting
   - `GenreViewSet` - Read-only genre list
   - `ActorViewSet` - Read-only actor list
   - `ReviewViewSet` - Review CRUD

4. **backend/movies/serializers.py** - Data serialization:
   - Serializers for all models
   - User registration serializer
   - Nested serializers for relationships

5. **backend/movies/urls/auth.py** - Authentication endpoints:
   - `/api/auth/register/` - User registration
   - `/api/auth/profile/` - Get user profile

### Frontend Files

1. **src/App.jsx** - Main app with React Router:
   - Routes for all pages
   - AuthProvider wrapper

2. **src/services/api.js** - API client:
   - Axios instance with interceptors
   - Token refresh handling
   - API methods for all endpoints

3. **src/contexts/AuthContext.jsx** - Authentication state:
   - User login/logout/register
   - Token management
   - Admin role checking

4. **src/pages/Home.jsx** - Home page:
   - Movie list with pagination
   - Search functionality
   - Filters (genre, year, rating)
   - Sorting options

5. **src/pages/MovieDetail.jsx** - Movie detail page:
   - Movie information display
   - Reviews list
   - Add review form

6. **src/pages/AdminPanel.jsx** - Admin panel:
   - Movie CRUD operations
   - CSV import
   - Poster upload

### DevOps Files

1. **docker-compose.yml** - Development setup:
   - PostgreSQL database
   - Django backend
   - React frontend with Nginx

2. **docker-compose.prod.yml** - Production setup:
   - Production-optimized services
   - Nginx reverse proxy
   - SSL support

3. **nginx.conf** - Development Nginx config:
   - Frontend serving
   - API proxying
   - Media file proxying

4. **nginx.prod.conf** - Production Nginx config:
   - SSL/TLS configuration
   - Security headers
   - Optimized caching

5. **.github/workflows/docker-build.yml** - CI/CD:
   - Docker image building
   - Container registry push
   - Multi-stage builds

## Environment Variables

All environment variables are documented in `env.example`. Key variables:

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (False for production)
- `ALLOWED_HOSTS` - Allowed hostnames
- `DB_*` - Database configuration
- `CORS_ALLOWED_ORIGINS` - CORS origins
- `SUPERUSER_*` - Superuser creation
- `VITE_API_URL` - Frontend API URL
- `VITE_MEDIA_URL` - Frontend media URL

## Quick Commands

### Development
```bash
docker-compose up --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py import_sample_data
```

### Production
```bash
docker-compose -f docker-compose.prod.yml up --build -d
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

## API Endpoints Summary

- `GET /api/movies/` - List movies (search, filter, pagination)
- `GET /api/movies/{id}/` - Movie details
- `POST /api/movies/` - Create movie (admin)
- `PATCH /api/movies/{id}/` - Update movie (admin)
- `DELETE /api/movies/{id}/` - Delete movie (admin)
- `POST /api/movies/import_csv/` - Import CSV (admin)
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create review
- `GET /api/genres/` - List genres
- `GET /api/actors/` - List actors
- `POST /api/auth/register/` - Register user
- `POST /api/auth/token/` - Login
- `POST /api/auth/token/refresh/` - Refresh token
- `GET /api/auth/profile/` - User profile

## Database Schema

- **User** (Django default) - Extended with reviews
- **Genre** - Movie genres (name, created_at)
- **Actor** - Movie actors (name, bio, birth_date)
- **Movie** - Movies (title, description, release_year, poster, genres M2M, actors M2M)
- **Review** - Reviews (user FK, movie FK, rating 1-10, text, created_at)

## Security Features

- JWT authentication
- CORS configuration
- CSRF protection
- SQL injection protection (Django ORM)
- XSS protection headers
- HTTPS enforcement in production
- Secure password validation
- Environment variable secrets









