# JustHD - Movie Streaming Platform

Premium movie streaming service built with Django REST Framework (Backend) and React (Frontend).

## Features
- User authentication with JWT
- Movie management with genres
- Comments and ratings system
- Premium subscription model
- Multi-language support
- Docker deployment
- Modern React frontend with Tailwind CSS

## Project Structure

```
JustHD/
├── core/              # Django project settings
├── apps/              # Django apps (users, movies, ratings, comments)
├── frontend/          # React frontend application
├── docker-compose.yml # Docker configuration
└── requirements.txt   # Python dependencies
```

## Quick Start

### Backend (Django)

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run `docker-compose up --build`
4. Access API at `http://localhost:8000`

### Frontend (React)

1. Navigate to `frontend` directory
2. Install dependencies: `npm install`
3. Create `.env` file with `VITE_API_BASE_URL=http://localhost:8000/api/v1`
4. Run `npm run dev`
5. Access frontend at `http://localhost:3000`

**For detailed frontend setup instructions, see [FRONTEND_SETUP.md](./FRONTEND_SETUP.md)**

## API Documentation
- Swagger UI: `/api/v1/docs/`
- ReDoc: `/api/v1/redoc/`

## Deployment

### Backend (DigitalOcean)
The Django backend can be deployed using Docker on DigitalOcean.

### Frontend
The React frontend can be deployed to:
- Vercel (recommended - easiest)
- Netlify
- GitHub Pages
- Or serve from your own server

See `frontend/README.md` for detailed deployment instructions.