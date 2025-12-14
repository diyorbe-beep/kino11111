import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(field_name='genres__slug', lookup_expr='exact')
    category = django_filters.CharFilter(field_name='categories__slug', lookup_expr='exact')
    content_type = django_filters.CharFilter(field_name='content_type', lookup_expr='exact')
    
    class Meta:
        model = Movie
        fields = ['genre', 'category', 'content_type', 'is_premium', 'release_year']