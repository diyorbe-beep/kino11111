from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from ..models import Category, Genre, Movie, Video, Episode
from ..serializers.admin import (
    AdminCategorySerializer, AdminGenreSerializer,
    AdminMovieSerializer, AdminVideoSerializer, AdminEpisodeSerializer
)
from apps.shared.utils.custom_response import CustomResponse
from apps.shared.permissions.base_permissions import IsAdminUser, IsSuperUser
from apps.ratings.models import Rating
from apps.comments.models import Comment
from apps.users.models import User

class AdminCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class AdminCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAdminUser]

class AdminGenreListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminGenreSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]

class AdminGenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = AdminGenreSerializer
    permission_classes = [IsAdminUser]

class AdminMovieListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminMovieSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'is_premium', 'is_premier', 'content_type']

    def get_queryset(self):
        return Movie.objects.prefetch_related('categories', 'genres')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=response.data
        )
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
        serializer.save()
        return CustomResponse.success(
            message_key="CREATED",
            request=request,
            data=serializer.data,
            status_code=201
        )

class AdminMovieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = AdminMovieSerializer
    permission_classes = [IsAdminUser]
    
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
        serializer.save()
        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=serializer.data
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse.success(
            message_key="DELETED",
            request=request,
            data={"message": "Movie deleted successfully"}
        )

class AdminVideoListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminVideoSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Video.objects.select_related('movie')

class AdminVideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = AdminVideoSerializer
    permission_classes = [IsAdminUser]

class AdminEpisodeListCreateView(generics.ListCreateAPIView):
    serializer_class = AdminEpisodeSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Episode.objects.select_related('tv_show')

class AdminEpisodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Episode.objects.all()
    serializer_class = AdminEpisodeSerializer
    permission_classes = [IsAdminUser]

class AdminDashboardView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        total_movies = Movie.objects.count()
        total_users = User.objects.count()
        total_views = Movie.objects.aggregate(total=Sum('views_count'))['total'] or 0
        total_ratings = Rating.objects.count()
        total_comments = Comment.objects.count()
        
        recent_movies = Movie.objects.order_by('-created_at')[:5]
        recent_users = User.objects.order_by('-date_joined')[:5]
        
        movies_by_category = Category.objects.annotate(
            movie_count=Count('movies')
        ).values('name', 'movie_count')
        
        views_by_day = Movie.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).extra({
            'date': "date(created_at)"
        }).values('date').annotate(
            views=Sum('views_count')
        ).order_by('date')
        
        data = {
            'statistics': {
                'total_movies': total_movies,
                'total_users': total_users,
                'total_views': total_views,
                'total_ratings': total_ratings,
                'total_comments': total_comments,
            },
            'recent_activity': {
                'movies': AdminMovieSerializer(recent_movies, many=True).data,
                'users': list(recent_users.values('id', 'username', 'email', 'date_joined')),
            },
            'charts': {
                'movies_by_category': list(movies_by_category),
                'views_by_day': list(views_by_day),
            }
        }
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=data
        )

class AdminBulkActionView(APIView):
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        action = request.data.get('action')
        movie_ids = request.data.get('movie_ids', [])
        
        if not action or not movie_ids:
            return CustomResponse.validation_error(
                errors={"detail": "Action and movie_ids are required"},
                request=request
            )
        
        movies = Movie.objects.filter(id__in=movie_ids)
        
        if action == 'activate':
            movies.update(is_active=True)
            message = f"{movies.count()} movies activated"
        elif action == 'deactivate':
            movies.update(is_active=False)
            message = f"{movies.count()} movies deactivated"
        elif action == 'mark_premium':
            movies.update(is_premium=True)
            message = f"{movies.count()} movies marked as premium"
        elif action == 'mark_free':
            movies.update(is_premium=False)
            message = f"{movies.count()} movies marked as free"
        elif action == 'mark_premier':
            movies.update(is_premier=True)
            message = f"{movies.count()} movies marked as premier"
        elif action == 'delete':
            count = movies.count()
            movies.delete()
            message = f"{count} movies deleted"
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

class AdminMovieAnalyticsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, movie_id=None):
        if movie_id:
            try:
                movie = Movie.objects.get(id=movie_id)
                
                total_views = movie.views_count
                total_ratings = movie.ratings.count()
                total_comments = movie.comments.count()
                avg_rating = movie.ratings.aggregate(avg=Avg('score'))['avg'] or 0
                
                views_by_date = []
                for i in range(30, 0, -1):
                    date = timezone.now() - timedelta(days=i)
                    views_by_date.append({
                        'date': date.date().isoformat(),
                        'views': 0
                    })
                
                data = {
                    'movie': AdminMovieSerializer(movie).data,
                    'statistics': {
                        'total_views': total_views,
                        'total_ratings': total_ratings,
                        'total_comments': total_comments,
                        'average_rating': round(avg_rating, 1),
                    },
                    'views_by_date': views_by_date,
                }
                
                return CustomResponse.success(
                    message_key="SUCCESS_MESSAGE",
                    request=request,
                    data=data
                )
            except Movie.DoesNotExist:
                return CustomResponse.not_found(request=request)
        
        movies = Movie.objects.annotate(
            rating_avg=Avg('ratings__score'),
            comments_count=Count('comments')
        ).order_by('-views_count')[:10]
        
        data = {
            'top_movies': AdminMovieSerializer(movies, many=True).data,
        }
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=data
        )