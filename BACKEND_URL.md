# Backend URL Configuration

Backend server: **http://139.59.137.138/**

## API Endpoints

- **API Base URL:** `http://139.59.137.138/api/v1/`
- **Media URL:** `http://139.59.137.138/media/`
- **Admin Panel:** `http://139.59.137.138/admin/`

## Frontend Configuration

Frontend `.env` faylida:
```
VITE_API_URL=http://139.59.137.138/api
VITE_MEDIA_URL=http://139.59.137.138/media
```

## CORS Settings

Backend `settings.py` da `CORS_ALLOWED_ORIGINS` ga frontend domain qo'shish kerak:

```python
CORS_ALLOWED_ORIGINS = [
    'http://139.59.137.138',
    'http://localhost:5173',
    'http://localhost:3000',
    # Frontend domain qo'shing
]
```

## Testing API

```bash
# Health check
curl http://139.59.137.138/health/

# API test
curl http://139.59.137.138/api/v1/genres/
```


