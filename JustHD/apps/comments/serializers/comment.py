from rest_framework import serializers
from apps.comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_avatar = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id', 'user', 'user_avatar', 'movie', 'movie_title', 
            'text', 'parent', 'replies', 'is_active', 
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def get_user_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None
    
    def get_replies(self, obj):
        if obj.replies.filter(is_active=True).exists():
            return CommentSerializer(
                obj.replies.filter(is_active=True), 
                many=True,
                context=self.context
            ).data
        return []

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('movie', 'text', 'parent')
    
    def validate_parent(self, value):
        if value and value.movie != self.initial_data.get('movie'):
            raise serializers.ValidationError({
                "parent": {
                    "en": "Parent comment must be for the same movie",
                    "uz": "Ota kommentariya xuddi shu kino uchun bo'lishi kerak",
                    "ru": "Родительский комментарий должен быть для того же фильма"
                }
            })
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        if 'user' in validated_data:
            validated_data.pop('user')

        parent = validated_data.pop('parent', None)
        
        return Comment.objects.create(user=user, parent=parent, **validated_data)
        
def validate(self, attrs):
    movie = attrs.get('movie')
    parent = attrs.get('parent')
    
    if parent and parent.movie != movie:
        raise serializers.ValidationError({
            "parent": {
                "en": "Parent comment must be for the same movie",
                "uz": "Ota kommentariya xuddi shu kino uchun bo'lishi kerak",
                "ru": "Родительский комментарий должен быть для того же фильма"
            }
        })
    
    return attrs