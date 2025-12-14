from django.urls import path
from ..views import views

app_name = 'ratings'

urlpatterns = [
    path('', views.RatingListView.as_view(), name='rating-list'),
    path('create/', views.RatingCreateView.as_view(), name='rating-create'),
    path('<int:pk>/', views.RatingDetailView.as_view(), name='rating-detail'),
    path('movie/<slug:movie_slug>/', views.MovieRatingsView.as_view(), name='movie-ratings'),
]