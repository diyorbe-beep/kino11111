#!/usr/bin/env python
"""
Script to seed categories and genres
"""

import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.movies.models import Category, Genre

def seed_categories():
    """Create default categories"""
    categories_data = [
        {
            'name': 'Movies',
            'name_uz': 'Filmlar',
            'name_ru': 'Фильмы',
            'description': 'Feature films and movies',
            'description_uz': 'Badiiy filmlar va kinolar',
            'description_ru': 'Художественные фильмы и кино',
            'icon': 'fas fa-film',
            'order': 1,
        },
        {
            'name': 'TV Shows',
            'name_uz': 'TV Dasturlar',
            'name_ru': 'ТВ Шоу',
            'description': 'Television series and shows',
            'description_uz': 'Televizion seriallar va shoular',
            'description_ru': 'Телевизионные сериалы и шоу',
            'icon': 'fas fa-tv',
            'order': 2,
        },
        {
            'name': 'Cartoons',
            'name_uz': 'Multfilmlar',
            'name_ru': 'Мультфильмы',
            'description': 'Animated cartoons and anime',
            'description_uz': 'Animatsion multfilmlar va anime',
            'description_ru': 'Анимационные мультфильмы и аниме',
            'icon': 'fas fa-child',
            'order': 3,
        },
        {
            'name': 'Documentaries',
            'name_uz': 'Hujjatli Filmlar',
            'name_ru': 'Документальные фильмы',
            'description': 'Documentary films and educational content',
            'description_uz': 'Hujjatli filmlar va o‘quv materiallari',
            'description_ru': 'Документальные фильмы и обучающий контент',
            'icon': 'fas fa-book',
            'order': 4,
        },
        {
            'name': 'Premier',
            'name_uz': 'Premyera',
            'name_ru': 'Премьера',
            'description': 'Newly released movies and shows',
            'description_uz': 'Yangi chiqqan filmlar va shoular',
            'description_ru': 'Новые фильмы и шоу',
            'icon': 'fas fa-star',
            'order': 5,
        },
    ]
    
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=data['name'].lower().replace(' ', '-'),
            defaults=data
        )
        if created:
            print(f"✅ Created category: {data['name']}")
        else:
            print(f"↻ Updated category: {data['name']}")

def seed_genres():
    """Create default genres"""
    genres_data = [
        # Action
        {'name': 'Action', 'name_uz': 'Jangari', 'name_ru': 'Боевик'},
        {'name': 'Adventure', 'name_uz': 'Sarguzasht', 'name_ru': 'Приключения'},
        {'name': 'Sci-Fi', 'name_uz': 'Ilmiy Fantastika', 'name_ru': 'Научная фантастика'},
        {'name': 'Fantasy', 'name_uz': 'Fantastika', 'name_ru': 'Фэнтези'},
        
        # Drama
        {'name': 'Drama', 'name_uz': 'Drama', 'name_ru': 'Драма'},
        {'name': 'Romance', 'name_uz': 'Romantika', 'name_ru': 'Романтика'},
        {'name': 'Comedy', 'name_uz': 'Komediya', 'name_ru': 'Комедия'},
        {'name': 'Horror', 'name_uz': 'Qo‘rqinchli', 'name_ru': 'Ужасы'},
        {'name': 'Thriller', 'name_uz': 'Triller', 'name_ru': 'Триллер'},
        {'name': 'Mystery', 'name_uz': 'Sir', 'name_ru': 'Мистика'},
        
        # Others
        {'name': 'Crime', 'name_uz': 'Jinoyat', 'name_ru': 'Криминал'},
        {'name': 'Biography', 'name_uz': 'Biografiya', 'name_ru': 'Биография'},
        {'name': 'History', 'name_uz': 'Tarix', 'name_ru': 'История'},
        {'name': 'War', 'name_uz': 'Urush', 'name_ru': 'Война'},
        {'name': 'Musical', 'name_uz': 'Musiqiy', 'name_ru': 'Мюзикл'},
        {'name': 'Family', 'name_uz': 'Oila', 'name_ru': 'Семейный'},
        {'name': 'Animation', 'name_uz': 'Animatsion', 'name_ru': 'Анимация'},
        {'name': 'Documentary', 'name_uz': 'Hujjatli', 'name_ru': 'Документальный'},
    ]
    
    for data in genres_data:
        genre, created = Genre.objects.get_or_create(
            slug=data['name'].lower().replace(' ', '-'),
            defaults=data
        )
        if created:
            print(f"✅ Created genre: {data['name']}")
        else:
            print(f"↻ Updated genre: {data['name']}")

if __name__ == '__main__':
    print("🌱 Seeding categories and genres...")
    seed_categories()
    seed_genres()
    print("✅ Seeding completed!")