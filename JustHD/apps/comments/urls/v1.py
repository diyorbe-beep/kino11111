from django.urls import path
from ..views import views

app_name = 'comments'

urlpatterns = [
    path('', views.CommentListView.as_view(), name='comment-list'),
    path('create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('<int:pk>/reply/', views.CommentReplyView.as_view(), name='comment-reply'),
    path('movie/<slug:movie_slug>/', views.MovieCommentsView.as_view(), name='movie-comments'),
]