from rest_framework import generics, permissions
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Count, Avg, Q, F
from django.utils import timezone
from ..filters import MovieFilter

from ..models import Category, Genre, Movie, MovieView, Episode
from ..serializers import (
    CategorySerializer, GenreSerializer, 
    MovieListSerializer, MovieDetailSerializer, 
    PremierMovieSerializer, EpisodeSerializer
)
from apps.shared.utils.custom_response import CustomResponse
from apps.shared.utils.decorators import premium_required
from django.utils.decorators import method_decorator

class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )

class GenreListView(generics.ListAPIView):
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Genre.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )


class MovieListView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categories', 'genres', 'content_type', 'is_premium', 'release_year']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'release_year', 'created_at', 'views_count', 'likes_count']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Movie.objects.filter(is_active=True).prefetch_related('categories', 'genres')
        
        user = self.request.user
        if not user.is_authenticated or not user.has_active_premium:
            queryset = queryset.filter(is_premium=False)

        genre_slug = self.request.query_params.get('genre')
        if genre_slug:
            queryset = queryset.filter(genres__slug=genre_slug)
        
        genre_id = self.request.query_params.get('genres')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        
        return queryset

class MovieDetailView(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        return Movie.objects.filter(is_active=True).prefetch_related(
            'categories', 'genres', 'videos', 'episodes'
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        MovieView.objects.create(
            movie=instance,
            user=request.user if request.user.is_authenticated else None,
            ip_address=self.get_client_ip(request)
        )

        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class MovieWatchView(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'

    def get_queryset(self):
        return Movie.objects.filter(is_active=True).prefetch_related('videos')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_premium and not request.user.has_active_premium:
            return CustomResponse.error(
                message_key="PREMIUM_REQUIRED",
                request=request,
                status_code=403
            )
        
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )

class PremierMoviesView(generics.ListAPIView):
    serializer_class = PremierMovieSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        now = timezone.now()
        queryset = Movie.objects.filter(
            is_premier=True,
            is_active=True,
            premier_date__lte=now
        )
        
        available_until = self.request.query_params.get('available_until')
        if available_until == 'active':
            queryset = queryset.filter(
                Q(available_until__isnull=True) | Q(available_until__gt=now)
            )
        
        return queryset.prefetch_related('categories', 'genres')
    
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

class FeaturedMoviesView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Movie.objects.filter(
            is_featured=True,
            is_active=True
        ).prefetch_related('categories', 'genres')
        
        user = self.request.user
        if not user.is_authenticated or not user.has_active_premium:
            queryset = queryset.filter(is_premium=False)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )

class TrendingMoviesView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = Movie.objects.filter(
            is_trending=True,
            is_active=True
        ).prefetch_related('categories', 'genres')
        
        user = self.request.user
        if not user.is_authenticated or not user.has_active_premium:
            queryset = queryset.filter(is_premium=False)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )

class SearchMoviesView(generics.ListAPIView):
    serializer_class = MovieListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()
        if not query:
            return Movie.objects.none()
        
        return Movie.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(categories__name__icontains=query)
        ).filter(is_active=True).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={
                'query': request.query_params.get('q', ''),
                'results': serializer.data,
                'count': len(serializer.data)
            }
        )

class TVShowEpisodesView(generics.ListAPIView):
    serializer_class = EpisodeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        tv_show_slug = self.kwargs['slug']
        season = self.request.query_params.get('season')
        
        queryset = Episode.objects.filter(
            tv_show__slug=tv_show_slug,
            tv_show__is_active=True
        )
        
        if season:
            queryset = queryset.filter(season_number=season)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )