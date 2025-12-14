from django.urls import path
from ..views import views
from ..views.admin_views import AdminMovieListCreateView, AdminMovieDetailView

app_name = 'movies'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('', views.MovieListView.as_view(), name='movie-list'),
    path('search/', views.SearchMoviesView.as_view(), name='movie-search'),
    path('featured/', views.FeaturedMoviesView.as_view(), name='featured-movies'),
    path('trending/', views.TrendingMoviesView.as_view(), name='trending-movies'),
    path('premier/', views.PremierMoviesView.as_view(), name='premier-movies'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('<slug:slug>/watch/', views.MovieWatchView.as_view(), name='movie-watch'),
    path('<slug:slug>/episodes/', views.TVShowEpisodesView.as_view(), name='tv-show-episodes'),
    # Admin endpoints for frontend admin panel
    path('create/', AdminMovieListCreateView.as_view(), name='movie-create'),
    path('<int:pk>/update/', AdminMovieDetailView.as_view(), name='movie-update'),
    path('<int:pk>/delete/', AdminMovieDetailView.as_view(), name='movie-delete'),
]