from pathlib import Path
from datetime import timedelta
from core import config
import os
import sys
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config.SECRET_KEY

# Security check: Ensure SECRET_KEY is changed in production
if not config.DEBUG:
    default_secrets = [
        'django-insecure-change-me-in-production',
        'your-secret-key-here-change-in-production',
        'change-me',
        ''
    ]
    if SECRET_KEY in default_secrets or len(SECRET_KEY) < 50:
        raise ValueError(
            "SECRET_KEY must be changed in production! "
            "Generate a new key with: "
            "python -c \"from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\""
        )

DEBUG = config.DEBUG

ALLOWED_HOSTS = config.ALLOWED_HOSTS

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'django_filters',
    'corsheaders',
    "debug_toolbar",
    # Apps
    'apps.shared',
    'apps.users',
    'apps.movies',
    'apps.ratings',
    'apps.comments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'apps.shared.middleware.LanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# Support for Render.com DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config.DB_NAME,
            'USER': config.DB_USER,
            'PASSWORD': config.DB_PASSWORD,
            'HOST': config.DB_HOST,
            'PORT': config.DB_PORT,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', 'English'),
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'uz', 'ru')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'uz', 'ru')

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = config.STATIC_ROOT

MEDIA_URL = 'media/'
MEDIA_ROOT = config.MEDIA_ROOT

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'apps.users.utils.custom_backend.MultiFieldBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config.JWT_ACCESS_LIFETIME),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=config.JWT_REFRESH_LIFETIME),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.shared.utils.custom_pagination.CustomPageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'EXCEPTION_HANDLER': 'apps.shared.exceptions.handler.custom_exception_handler',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'JustHD - Movie Streaming Platform',
    'DESCRIPTION': 'Premium movie streaming service API documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v1/',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayRequestDuration': True,
    },
}

# CORS settings - Moslashuvchan sozlamalar
import re

# Belgilangan originlar
frontend_urls = config.FRONTEND_URLS if isinstance(config.FRONTEND_URLS, list) else []

# Development va Production rejimlari uchun alohida CORS sozlamalari
if DEBUG:
    # Development rejimida barcha localhost va local network portlarini ruxsat berish
    CORS_ALLOWED_ORIGIN_REGEXES = [
        re.compile(r'^http://localhost:\d+$'),
        re.compile(r'^http://127\.0\.0\.1:\d+$'),
        re.compile(r'^http://192\.168\.\d+\.\d+:\d+$'),  # Local network
        re.compile(r'^http://10\.\d+\.\d+\.\d+:\d+$'),  # Local network
    ]
    # Belgilangan originlar ham qo'shiladi
    CORS_ALLOWED_ORIGINS = frontend_urls
else:
    # Production rejimida belgilangan production originlar
    # Localhost URL'larini olib tashlash - security uchun
    production_urls = [
        url for url in frontend_urls 
        if not url.startswith('http://localhost') 
        and not url.startswith('http://127.0.0.1')
    ]
    
    if not production_urls:
        # Agar production URL'lar bo'sh bo'lsa, xato qaytarish
        import warnings
        warnings.warn(
            "CORS_ALLOWED_ORIGINS is empty or contains only localhost URLs in production! "
            "Please set CORS_ALLOWED_ORIGINS in environment variables with production URLs.",
            UserWarning
        )
        # Xavfsizlik uchun, agar production URL'lar bo'sh bo'lsa, default URL'larni ishlatish
        # Lekin bu faqat development uchun, production'da xato qaytarish kerak
        CORS_ALLOWED_ORIGINS = frontend_urls if frontend_urls else []
    else:
        CORS_ALLOWED_ORIGINS = production_urls
    
    CORS_ALLOWED_ORIGIN_REGEXES = []

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_EXPOSE_HEADERS = ['Content-Type', 'Authorization']
CORS_PREFLIGHT_MAX_AGE = 86400

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
    LOGGING = {}
    config.TELEGRAM_BOT_TOKEN = None
    config.TELEGRAM_CHANNEL_ID = None

os.makedirs(BASE_DIR / 'logs', exist_ok=True)