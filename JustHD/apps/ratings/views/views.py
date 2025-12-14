from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from ..models import Rating
from ..serializers import RatingSerializer, RatingCreateSerializer
from apps.shared.utils.custom_response import CustomResponse

class RatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['movie', 'user', 'score']
    ordering_fields = ['score', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Rating.objects.select_related('user', 'movie')

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

class RatingCreateView(generics.CreateAPIView):
    serializer_class = RatingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
            
        rating = serializer.save()
        
        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=RatingSerializer(rating, context={'request': request}).data
        )

class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)
    
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
            data=RatingSerializer(instance, context={'request': request}).data
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return CustomResponse.success(
            message_key="DELETED",
            request=request,
            data={"message": "Rating deleted successfully"}
        )

class MovieRatingsView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        movie_slug = self.kwargs['movie_slug']
        return Rating.objects.filter(
            movie__slug=movie_slug
        ).select_related('user', 'movie')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )