from django.urls import path
from ..views.admin_views import (
    AdminCategoryListCreateView, AdminCategoryDetailView,
    AdminGenreListCreateView, AdminGenreDetailView,
    AdminMovieListCreateView, AdminMovieDetailView,
    AdminVideoListCreateView, AdminVideoDetailView,
    AdminEpisodeListCreateView, AdminEpisodeDetailView,
    AdminDashboardView, AdminBulkActionView, AdminMovieAnalyticsView
)

app_name = 'admin_movies'

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='dashboard'),
    
    path('categories/', AdminCategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:pk>/', AdminCategoryDetailView.as_view(), name='category-detail'),
    
    path('genres/', AdminGenreListCreateView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', AdminGenreDetailView.as_view(), name='genre-detail'),
    
    path('movies/', AdminMovieListCreateView.as_view(), name='movie-list'),
    path('movies/<int:pk>/', AdminMovieDetailView.as_view(), name='movie-detail'),
    path('movies/bulk-actions/', AdminBulkActionView.as_view(), name='movie-bulk-actions'),
    path('movies/analytics/', AdminMovieAnalyticsView.as_view(), name='movie-analytics'),
    path('movies/analytics/<int:movie_id>/', AdminMovieAnalyticsView.as_view(), name='movie-analytics-detail'),
    
    path('videos/', AdminVideoListCreateView.as_view(), name='video-list'),
    path('videos/<int:pk>/', AdminVideoDetailView.as_view(), name='video-detail'),
    
    path('episodes/', AdminEpisodeListCreateView.as_view(), name='episode-list'),
    path('episodes/<int:pk>/', AdminEpisodeDetailView.as_view(), name='episode-detail'),
]