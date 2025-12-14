from rest_framework import serializers
from apps.movies.models import Episode

class EpisodeSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Episode
        fields = ('id', 'tv_show', 'season_number', 'episode_number', 'title', 'description', 'duration', 'created_at')
    
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