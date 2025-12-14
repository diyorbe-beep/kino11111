from rest_framework import serializers
from apps.movies.models import Movie
from .category import CategorySerializer
from .genre import GenreSerializer
from .video import VideoSerializer
from .episode import EpisodeSerializer

class MovieListSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'slug', 'description', 'release_year', 
            'duration', 'content_type', 'age_rating', 'poster',
            'is_premium', 'is_premier', 'is_featured', 'is_trending',
            'categories', 'genres', 'average_rating', 'imdb_rating',
            'views_count', 'likes_count', 'created_at'
        )
    
    def get_title(self, obj):
        return self._get_translated_field(obj, 'title')
    
    def get_description(self, obj):
        return self._get_translated_field(obj, 'description')
    
    def get_average_rating(self, obj):
        return obj.average_rating
    
    def _get_translated_field(self, obj, field):
        request = self.context.get('request')
        lang = 'en'
        if request and hasattr(request, 'lang'):
            lang = request.lang
        elif request:
            accept_lang = request.headers.get('Accept-Language', 'en')
            lang = accept_lang.split(';')[0].split(',')[0].strip()[:2]
        
        field_key = f"{field}_{lang}"
        if hasattr(obj, field_key):
            value = getattr(obj, field_key, '')
            return value if value else getattr(obj, field)
        return getattr(obj, field)

class MovieDetailSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    videos = VideoSerializer(many=True, read_only=True)
    episodes = EpisodeSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_watched = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'slug', 'description', 'poster', 
            'release_year', 'duration', 'content_type', 'age_rating',
            'trailer_url', 'is_premium', 'is_premier', 'premier_date',
            'available_until', 'is_featured', 'is_trending',
            'categories', 'genres', 'videos', 'episodes', 
            'views_count', 'likes_count', 'imdb_rating',
            'average_rating', 'comments_count', 'is_watched',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_title(self, obj):
        return self._get_translated_field(obj, 'title')
    
    def get_description(self, obj):
        return self._get_translated_field(obj, 'description')
    
    def get_average_rating(self, obj):
        return obj.average_rating
    
    def get_comments_count(self, obj):
        from apps.comments.models import Comment
        return Comment.objects.filter(movie=obj, is_active=True).count()
    
    def get_is_watched(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            from apps.movies.models import MovieView
            return MovieView.objects.filter(movie=obj, user=request.user).exists()
        return False
    
    def _get_translated_field(self, obj, field):
        request = self.context.get('request')
        lang = 'en'
        if request and hasattr(request, 'lang'):
            lang = request.lang
        elif request:
            accept_lang = request.headers.get('Accept-Language', 'en')
            lang = accept_lang.split(';')[0].split(',')[0].strip()[:2]
        
        field_key = f"{field}_{lang}"
        if hasattr(obj, field_key):
            value = getattr(obj, field_key, '')
            return value if value else getattr(obj, field)
        return getattr(obj, field)

class PremierMovieSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'slug', 'description', 'poster',
            'release_year', 'duration', 'content_type',
            'is_premium', 'premier_date', 'available_until',
            'categories', 'genres', 'views_count', 'likes_count',
            'created_at'
        )
    
    def get_title(self, obj):
        return self._get_translated_field(obj, 'title')
    
    def get_description(self, obj):
        return self._get_translated_field(obj, 'description')
    
    def _get_translated_field(self, obj, field):
        request = self.context.get('request')
        lang = 'en'
        if request and hasattr(request, 'lang'):
            lang = request.lang
        elif request:
            accept_lang = request.headers.get('Accept-Language', 'en')
            lang = accept_lang.split(';')[0].split(',')[0].strip()[:2]
        
        field_key = f"{field}_{lang}"
        if hasattr(obj, field_key):
            value = getattr(obj, field_key, '')
            return value if value else getattr(obj, field)
        return getattr(obj, field)