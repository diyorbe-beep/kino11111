from rest_framework import serializers
from ..models import Category, Genre, Movie, Video, Episode

class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AdminGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class AdminVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class AdminEpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'

class AdminMovieSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Category.objects.all(),
        required=False
    )
    genres = serializers.PrimaryKeyRelatedField(
        many=True, 
        queryset=Genre.objects.all(),
        required=False
    )
    
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'poster': {'required': False},
            'trailer_url': {'required': False},
            'imdb_rating': {'required': False},
            'premier_date': {'required': False},
            'available_until': {'required': False},
        }
    
    def validate(self, attrs):
        if 'poster' not in attrs:
            attrs['poster'] = None
        return attrs