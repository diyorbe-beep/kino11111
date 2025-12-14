from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from ..models import Comment
from ..serializers import CommentSerializer, CommentCreateSerializer
from apps.shared.utils.custom_response import CustomResponse

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['movie', 'user']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Comment.objects.filter(
            is_active=True, 
            parent__isnull=True
        ).select_related('user', 'movie').prefetch_related('replies')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
            
        comment = serializer.save()
        
        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=CommentSerializer(comment, context={'request': request}).data
        )

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.method == 'GET':
            return Comment.objects.filter(is_active=True)
        return Comment.objects.filter(user=self.request.user, is_active=True)
    
    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
            
        self.perform_update(serializer)
        
        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=CommentSerializer(instance, context={'request': request}).data
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return CustomResponse.success(
            message_key="DELETED",
            request=request,
            data={"message": "Comment deleted successfully"}
        )
    
class CommentReplyView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            parent_comment = Comment.objects.get(pk=kwargs['pk'])
        except Comment.DoesNotExist:
            return CustomResponse.not_found(
                message_key="COMMENT_NOT_FOUND",
                request=request
            )
            
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )

        if serializer.validated_data['movie'] != parent_comment.movie:
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                request=request,
                errors={"movie": {
                    "en": "Reply must be for the same movie",
                    "uz": "Javob xuddi shu kino uchun bo'lishi kerak",
                    "ru": "Ответ должен быть для того же фильма"
                }}
            )
        
        comment = serializer.save(user=request.user, parent=parent_comment)
        
        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=CommentSerializer(comment, context={'request': request}).data
        )
    
class MovieCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_slug = self.kwargs['movie_slug']
        return Comment.objects.filter(
            movie__slug=movie_slug,
            is_active=True,
            parent__isnull=True
        ).select_related('user', 'movie').prefetch_related('replies')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )