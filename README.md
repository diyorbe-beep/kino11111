# IMDb-Style Movie Website

A full-stack movie database application built with Django REST Framework backend and React (Vite) frontend, featuring user authentication, movie management, reviews, and admin panel.

## Features

- **Backend (Django REST API)**
  - JWT authentication
  - Movie CRUD operations
  - Review system with ratings (1-10)
  - Search, filter, sorting, and pagination
  - CSV import for movies
  - Image upload for movie posters
  - Admin and user roles

- **Frontend (React + Vite)**
  - Responsive design
  - User authentication (register/login/logout)
  - Movie browsing with filters
  - Movie detail pages with reviews
  - Admin panel for movie management
  - User profile page

## Tech Stack

- **Backend**: Django 4.2+, Django REST Framework, PostgreSQL, JWT
- **Frontend**: React 19, React Router, Axios, Vite
- **DevOps**: Docker, Docker Compose, Nginx, Gunicorn

## Project Structure

```
.
├── backend/                 # Django backend
│   ├── config/            # Django project settings
│   ├── movies/            # Movies app
│   │   ├── models.py      # Database models
│   │   ├── serializers.py # API serializers
│   │   ├── views.py       # API views
│   │   └── urls/          # URL routing
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── src/                    # React frontend
│   ├── components/         # Reusable components
│   ├── pages/              # Page components
│   ├── services/           # API service
│   └── contexts/           # React contexts
├── docker-compose.yml      # Development setup
├── docker-compose.prod.yml # Production setup
├── nginx.conf              # Nginx config for dev
├── nginx.prod.conf         # Nginx config for production
└── README.md
```

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kino
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your configuration values.

3. **Build and start services**
   ```bash
   docker-compose up --build
   ```

4. **Run migrations**
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```
   Or use the management command:
   ```bash
   docker-compose exec backend python manage.py create_superuser
   ```

6. **Import sample data (optional)**
   ```bash
   docker-compose exec backend python manage.py import_sample_data
   ```

7. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000/api/
   - Admin Panel: http://localhost:8000/admin/

### Production Deployment

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Update all values in `.env` for production:
   - Set `DEBUG=False`
   - Set `SECRET_KEY` to a secure random string
   - Configure `ALLOWED_HOSTS` with your domain
   - Set database credentials
   - Update `CORS_ALLOWED_ORIGINS` with your frontend URL

2. **Build and start services**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Run migrations**
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
   ```

4. **Collect static files**
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
   ```

5. **Create superuser**
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
   ```

6. **Set up SSL (Let's Encrypt)**
   ```bash
   # Install certbot
   sudo apt-get update
   sudo apt-get install certbot

   # Obtain certificate
   sudo certbot certonly --standalone -d example.com -d www.example.com

   # Copy certificates to project
   sudo cp /etc/letsencrypt/live/example.com/fullchain.pem ./ssl/
   sudo cp /etc/letsencrypt/live/example.com/privkey.pem ./ssl/
   sudo chown $USER:$USER ./ssl/*.pem
   ```

7. **Restart nginx service**
   ```bash
   docker-compose -f docker-compose.prod.yml restart nginx
   ```

## Management Commands

### Create Superuser from Environment Variables
```bash
docker-compose exec backend python manage.py create_superuser
```
Uses `SUPERUSER_USERNAME`, `SUPERUSER_EMAIL`, and `SUPERUSER_PASSWORD` from `.env`.

### Import Sample Data
```bash
docker-compose exec backend python manage.py import_sample_data
```
Creates sample genres, actors, movies, and reviews.

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get current user profile

### Movies
- `GET /api/movies/` - List movies (with search, filter, pagination)
- `GET /api/movies/{id}/` - Get movie details
- `POST /api/movies/` - Create movie (admin only)
- `PATCH /api/movies/{id}/` - Update movie (admin only)
- `DELETE /api/movies/{id}/` - Delete movie (admin only)
- `POST /api/movies/import_csv/` - Import movies from CSV (admin only)

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create review (authenticated)
- `PATCH /api/reviews/{id}/` - Update review (own reviews only)
- `DELETE /api/reviews/{id}/` - Delete review (own reviews only)

### Genres & Actors
- `GET /api/genres/` - List all genres
- `GET /api/actors/` - List all actors

### Query Parameters

**Movies endpoint supports:**
- `search` - Search in title, description, actor names
- `genres` - Filter by genre ID
- `release_year` - Filter by year
- `min_rating` - Minimum average rating
- `max_rating` - Maximum average rating
- `ordering` - Sort by: `title`, `-title`, `release_year`, `-release_year`, `created_at`, `-created_at`, `average_rating`, `-average_rating`
- `page` - Page number for pagination

## CSV Import Format

CSV file should have the following columns:
- `title` - Movie title (required)
- `description` - Movie description (required)
- `release_year` - Release year (required)
- `genres` - Comma-separated genre names
- `actors` - Comma-separated actor names

Example:
```csv
title,description,release_year,genres,actors
The Matrix,A computer hacker learns about the true nature of reality,1999,"Action, Sci-Fi","Keanu Reeves, Laurence Fishburne"
```

## Media Storage

### Development
Media files are stored locally in `backend/media/` directory.

### Production
For production, consider using:
- **AWS S3** - Use `django-storages` package
- **MinIO** - Self-hosted S3-compatible storage
- **NFS/Shared Volume** - For multi-container deployments

Example S3 configuration (add to `settings.py`):
```python
INSTALLED_APPS += ['storages']
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
```

## Environment Variables

See `.env.example` for all available environment variables.

### Required for Production
- `SECRET_KEY` - Django secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG=False`
- `ALLOWED_HOSTS` - Your domain(s)
- `DB_PASSWORD` - Secure database password
- `CORS_ALLOWED_ORIGINS` - Your frontend URL(s)

### Optional: Telegram Bot for Error Alerts
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token (get from @BotFather)
- `TELEGRAM_CHANNEL_ID` - Your Telegram channel ID where errors will be sent

**To set up Telegram bot:**
1. Create a bot with @BotFather on Telegram
2. Get your bot token
3. Create a channel and add your bot as administrator
4. Get channel ID (you can use @userinfobot or forward a message from channel to @getidsbot)
5. Add both values to `.env` file

When errors occur in production (DEBUG=False), they will be automatically sent to your Telegram channel.

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check database credentials in `.env`
- Verify network connectivity: `docker-compose exec backend ping db`

### Static Files Not Loading
- Run `collectstatic`: `docker-compose exec backend python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `MEDIA_ROOT` settings
- Verify volume mounts in `docker-compose.yml`

### CORS Errors
- Update `CORS_ALLOWED_ORIGINS` in `.env`
- Restart backend: `docker-compose restart backend`

### Frontend Build Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Check `VITE_API_URL` and `VITE_MEDIA_URL` in build args

## Development

### Running Backend Tests
```bash
docker-compose exec backend python manage.py test
```

### Accessing Django Shell
```bash
docker-compose exec backend python manage.py shell
```

### Viewing Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Database Backup
```bash
docker-compose exec db pg_dump -U postgres movie_db > backup.sql
```

### Database Restore
```bash
docker-compose exec -T db psql -U postgres movie_db < backup.sql
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
