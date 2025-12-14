from django.urls import path
from ..views.admin_views import (
    AdminCommentListView, AdminCommentDetailView, AdminCommentBulkActionView
)

app_name = 'admin_comments'

urlpatterns = [
    path('comments/', AdminCommentListView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', AdminCommentDetailView.as_view(), name='comment-detail'),
    path('comments/bulk-actions/', AdminCommentBulkActionView.as_view(), name='comment-bulk-actions'),
]