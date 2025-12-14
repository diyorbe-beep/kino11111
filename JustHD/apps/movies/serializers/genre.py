from rest_framework import serializers
from apps.movies.models import Genre

class GenreSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug', 'description', 'created_at')
    
    def get_name(self, obj):
        request = self.context.get('request')
        lang = 'en'
        if request and hasattr(request, 'lang'):
            lang = request.lang
        elif request:
            accept_lang = request.headers.get('Accept-Language', 'en')
            lang = accept_lang.split(';')[0].split(',')[0].strip()[:2]

        if lang == 'uz' and hasattr(obj, 'name_uz') and obj.name_uz:
            return obj.name_uz
        elif lang == 'ru' and hasattr(obj, 'name_ru') and obj.name_ru:
            return obj.name_ru
        return obj.name
    
    def get_description(self, obj):
        request = self.context.get('request')
        lang = 'en'
        if request and hasattr(request, 'lang'):
            lang = request.lang
        elif request:
            accept_lang = request.headers.get('Accept-Language', 'en')
            lang = accept_lang.split(';')[0].split(',')[0].strip()[:2]

        if lang == 'uz' and hasattr(obj, 'description_uz') and obj.description_uz:
            return obj.description_uz
        elif lang == 'ru' and hasattr(obj, 'description_ru') and obj.description_ru:
            return obj.description_ru
        return obj.description