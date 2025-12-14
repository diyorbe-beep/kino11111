from rest_framework import serializers
from apps.ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Rating
        fields = (
            'id', 'user', 'movie', 'movie_title', 'score', 
            'comment', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('movie', 'score', 'comment')
    
    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError({
                "score": {
                    "en": "Score must be between 1 and 10",
                    "uz": "Reyting 1 dan 10 gacha bo'lishi kerak",
                    "ru": "Оценка должна быть от 1 до 10"
                }
            })
        return value
    
    def validate(self, attrs):
        user = self.context['request'].user
        movie = attrs.get('movie')
        
        if Rating.objects.filter(user=user, movie=movie).exists():
            raise serializers.ValidationError({
                "non_field_errors": {
                    "en": "You have already rated this movie",
                    "uz": "Siz bu kinoni allaqachon baholagansiz",
                    "ru": "Вы уже оценили этот фильм"
                }
            })
        
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Rating.objects.create(user=user, **validated_data)