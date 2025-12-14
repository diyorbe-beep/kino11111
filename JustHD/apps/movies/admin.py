from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline, TranslationTabularInline
from .models import Category, Genre, Movie, Video, MovieView, Episode

class VideoInline(TranslationTabularInline):
    model = Video
    extra = 1
    fields = ('quality', 'language', 'subtitle_language', 'video_file', 'is_active')
    verbose_name = _('Video')
    verbose_name_plural = _('Videos')

class EpisodeInline(TranslationStackedInline):
    model = Episode
    extra = 1
    fields = ('season_number', 'episode_number', 'title', 'description', 'duration')
    verbose_name = _('Episode')
    verbose_name_plural = _('Episodes')

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('title', 'release_year', 'content_type', 'is_premium', 'is_active', 'is_premier', 'views_count')
    list_filter = ('content_type', 'is_premium', 'is_active', 'is_premier', 'is_featured', 'is_trending', 'genres', 'release_year')
    search_fields = ('title', 'description')
    filter_horizontal = ('categories', 'genres')
    readonly_fields = ('views_count', 'likes_count', 'created_at', 'updated_at', 'poster_preview')
    inlines = [VideoInline, EpisodeInline]
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'description', 'content_type', 'age_rating')
        }),
        (_('Media'), {
            'fields': ('poster', 'poster_preview', 'trailer_url')
        }),
        (_('Details'), {
            'fields': ('release_year', 'duration', 'imdb_rating')
        }),
        (_('Categories & Genres'), {
            'fields': ('categories', 'genres')
        }),
        (_('Premier Information'), {
            'fields': ('is_premier', 'premier_date', 'available_until')
        }),
        (_('Status & Flags'), {
            'fields': ('is_premium', 'is_active', 'is_featured', 'is_trending')
        }),
        (_('Statistics'), {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def poster_preview(self, obj):
        if obj.poster:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.poster.url)
        return "-"
    poster_preview.short_description = _('Poster Preview')
    
    actions = ['make_premium', 'make_free', 'mark_as_featured', 'mark_as_trending', 'mark_as_premier']
    
    def make_premium(self, request, queryset):
        queryset.update(is_premium=True)
        self.message_user(request, _("Selected movies marked as premium"))
    make_premium.short_description = _("Mark selected as premium")
    
    def make_free(self, request, queryset):
        queryset.update(is_premium=False)
        self.message_user(request, _("Selected movies marked as free"))
    make_free.short_description = _("Mark selected as free")
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, _("Selected movies marked as featured"))
    mark_as_featured.short_description = _("Mark selected as featured")
    
    def mark_as_trending(self, request, queryset):
        queryset.update(is_trending=True)
        self.message_user(request, _("Selected movies marked as trending"))
    mark_as_trending.short_description = _("Mark selected as trending")
    
    def mark_as_premier(self, request, queryset):
        queryset.update(is_premier=True)
        self.message_user(request, _("Selected movies marked as premier"))
    mark_as_premier.short_description = _("Mark selected as premier")

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('movie', 'quality', 'language', 'size', 'is_active', 'created_at')
    list_filter = ('quality', 'language', 'is_active', 'created_at')
    search_fields = ('movie__title',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('movie', 'quality', 'language', 'subtitle_language')
        }),
        ('Media', {
            'fields': ('video_file', 'thumbnail', 'size', 'duration')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MovieView)
class MovieViewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'ip_address', 'duration_watched', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('movie__title', 'user__username', 'ip_address')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Episode)
class EpisodeAdmin(TranslationAdmin):
    list_display = ('tv_show', 'season_number', 'episode_number', 'title', 'duration', 'created_at')
    list_filter = ('season_number', 'tv_show')
    search_fields = ('title', 'description', 'tv_show__title')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('tv_show', 'season_number', 'episode_number')
        }),
        ('Content', {
            'fields': ('title', 'description', 'duration')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )