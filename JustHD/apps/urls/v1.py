from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.users.urls.v1')),
    path('movies/', include('apps.movies.urls.v1')),
    path('admin/movies/', include('apps.movies.urls.admin_v1')),
    path('admin/comments/', include('apps.comments.urls.admin_v1')),
    path('admin/ratings/', include('apps.ratings.urls.admin_v1')),
    path('ratings/', include('apps.ratings.urls.v1')),
    path('comments/', include('apps.comments.urls.v1')),
]