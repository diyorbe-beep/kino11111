from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Genre, Movie, Video, Episode

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'uz', 'ru')

class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
    required_languages = ('en', 'uz', 'ru')

class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('en', 'uz', 'ru')

class VideoTranslationOptions(TranslationOptions):
    fields = ()

class EpisodeTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
    required_languages = ('en', 'uz', 'ru')

translator.register(Category, CategoryTranslationOptions)
translator.register(Genre, GenreTranslationOptions)
translator.register(Movie, MovieTranslationOptions)
translator.register(Video, VideoTranslationOptions)
translator.register(Episode, EpisodeTranslationOptions)