from django.urls import path
from ..views.admin_views import (
    AdminRatingListView, AdminRatingDetailView, AdminRatingBulkActionView
)

app_name = 'admin_ratings'

urlpatterns = [
    path('ratings/', AdminRatingListView.as_view(), name='rating-list'),
    path('ratings/<int:pk>/', AdminRatingDetailView.as_view(), name='rating-detail'),
    path('ratings/bulk-actions/', AdminRatingBulkActionView.as_view(), name='rating-bulk-actions'),
]