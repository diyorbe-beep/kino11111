"""
URL configuration for core project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView

from apps.shared.utils.decorators import superuser_required

def home(request):
    return JsonResponse({
        "message": "JustHD API is running",
        "version": "1.0.0",
    })

def test_auth(request):
    """Test endpoint to verify auth URLs are working"""
    return JsonResponse({
        "message": "Auth URLs are working",
        "endpoint": "/api/v1/auth/token/",
        "status": "ok"
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls.v1')),
    path('api/v1/test-auth/', test_auth, name='test-auth'),  # Test endpoint
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

schema_view = SpectacularSwaggerView.as_view(url_name='schema')
redoc_view = SpectacularRedocView.as_view(url_name='schema')

urlpatterns += [
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
]

if settings.DEBUG:
    urlpatterns += [
        path("api/v1/docs/", schema_view, name="swagger-ui"),
        path("api/v1/redoc/", redoc_view, name="redoc"),
    ]
else:
    urlpatterns += [
        path("api/v1/docs/", superuser_required(schema_view), name="swagger-ui"),
        path("api/v1/redoc/", superuser_required(redoc_view), name="redoc"),
    ]

# Health check endpoint (optional)
try:
    from health_check import urls as health_check_urls
    urlpatterns += [
        path('health/', include(health_check_urls)),
    ]
except ImportError:
    # Health check not installed, create simple endpoint
    def health_check(request):
        from django.http import JsonResponse
        return JsonResponse({'status': 'ok', 'service': 'JustHD API'})
    urlpatterns += [
        path('health/', health_check, name='health-check'),
    ]

if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass