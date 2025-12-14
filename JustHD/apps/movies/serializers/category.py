from rest_framework import serializers
from apps.movies.models import Category

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon', 'order', 'is_active', 'created_at')
    
    def get_name(self, obj):
        request = self.context.get('request')
        lang = self._get_language(request)
        return self._get_translated_field(obj, 'name', lang)
    
    def get_description(self, obj):
        request = self.context.get('request')
        lang = self._get_language(request)
        return self._get_translated_field(obj, 'description', lang)
    
    def _get_language(self, request):
        if request and hasattr(request, 'lang'):
            return request.lang
        if request and hasattr(request, 'headers'):
            accept_lang = request.headers.get('Accept-Language', 'en')
            return accept_lang.split(';')[0].split(',')[0].strip()[:2]
        return 'en'
    
    def _get_translated_field(self, obj, field, lang):
        field_key = f"{field}_{lang}"
        if hasattr(obj, field_key):
            value = getattr(obj, field_key, '')
            return value if value else getattr(obj, field)
        return getattr(obj, field)