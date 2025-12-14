from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Comment
from ..serializers import CommentSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.shared.permissions.base_permissions import IsAdminUser

class AdminCommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'movie', 'user']
    
    def get_queryset(self):
        return Comment.objects.select_related('user', 'movie')

class AdminCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

class AdminCommentBulkActionView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        action = request.data.get('action')
        comment_ids = request.data.get('comment_ids', [])
        
        if not action or not comment_ids:
            return CustomResponse.validation_error(
                errors={"detail": "Action and comment_ids are required"},
                request=request
            )
        
        comments = Comment.objects.filter(id__in=comment_ids)
        
        if action == 'activate':
            comments.update(is_active=True)
            message = f"{comments.count()} comments activated"
        elif action == 'deactivate':
            comments.update(is_active=False)
            message = f"{comments.count()} comments deactivated"
        elif action == 'delete':
            count = comments.count()
            comments.delete()
            message = f"{count} comments deleted"
        else:
            return CustomResponse.validation_error(
                errors={"detail": "Invalid action"},
                request=request
            )
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={"message": message}
        )