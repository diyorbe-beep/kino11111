from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from ..models import Rating
from ..serializers import RatingSerializer
from apps.shared.utils.custom_response import CustomResponse
from apps.shared.permissions.base_permissions import IsAdminUser

class AdminRatingListView(generics.ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['movie', 'user', 'score']
    
    def get_queryset(self):
        return Rating.objects.select_related('user', 'movie')

class AdminRatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAdminUser]

class AdminRatingBulkActionView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        rating_ids = request.data.get('rating_ids', [])
        
        if not rating_ids:
            return CustomResponse.validation_error(
                errors={"detail": "rating_ids are required"},
                request=request
            )
        
        ratings = Rating.objects.filter(id__in=rating_ids)
        count = ratings.count()
        ratings.delete()
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={"message": f"{count} ratings deleted"}
        )