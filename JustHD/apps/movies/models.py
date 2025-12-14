from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.shared.models import BaseModel

class Category(BaseModel):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True, null=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True, null=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Genre(BaseModel):
    name = models.CharField(_('name'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'), blank=True, null=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='genres',
        verbose_name=_('category')
    )
    
    class Meta:
        db_table = 'genres'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Movie(BaseModel):
    CONTENT_TYPES = [
        ('movie', _('Movie')),
        ('tv_show', _('TV Show')),
        ('cartoon', _('Cartoon')),
        ('documentary', _('Documentary')),
        ('anime', _('Anime')),
    ]
    
    AGE_RATINGS = [
        ('G', _('G - All Ages')),
        ('PG', _('PG - Parental Guidance')),
        ('PG-13', _('PG-13 - Parents Strongly Cautioned')),
        ('R', _('R - Restricted')),
        ('NC-17', _('NC-17 - Adults Only')),
    ]
    
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), unique=True, blank=True)
    description = models.TextField(_('description'))
    release_year = models.IntegerField(_('release year'), validators=[
        MinValueValidator(1900), 
        MaxValueValidator(2100)
    ])
    duration = models.IntegerField(_('duration'), help_text=_("Duration in minutes"))
    content_type = models.CharField(_('content type'), max_length=20, choices=CONTENT_TYPES, default='movie')
    age_rating = models.CharField(_('age rating'), max_length=10, choices=AGE_RATINGS, default='PG-13')
    
    poster = models.ImageField(
        _('poster'), 
        upload_to='movie_posters/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text=_("Poster image file")
    )
    trailer_url = models.URLField(_('trailer url'), blank=True, null=True)
    imdb_rating = models.DecimalField(_('IMDb rating'), max_digits=3, decimal_places=1, blank=True, null=True)
    
    is_premium = models.BooleanField(_('is premium'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_trending = models.BooleanField(_('is trending'), default=False)
    
    views_count = models.PositiveIntegerField(_('views count'), default=0)
    likes_count = models.PositiveIntegerField(_('likes count'), default=0)
    
    categories = models.ManyToManyField(Category, related_name='movies', verbose_name=_('categories'), blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', verbose_name=_('genres'))
    
    is_premier = models.BooleanField(_('is premier'), default=False)
    premier_date = models.DateTimeField(_('premier date'), blank=True, null=True)
    available_until = models.DateTimeField(_('available until'), blank=True, null=True)
    
    class Meta:
        db_table = 'movies'
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_premium', 'is_active']),
            models.Index(fields=['release_year']),
            models.Index(fields=['is_premier', 'premier_date']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_trending']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.release_year})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def average_rating(self):
        from apps.ratings.models import Rating
        ratings = self.ratings.all()
        if ratings:
            avg = sum(rating.score for rating in ratings) / len(ratings)
            return round(avg, 1)
        return 0

class Video(BaseModel):
    QUALITY_CHOICES = [
        ('SD', _('SD (480p)')),
        ('HD', _('HD (720p)')),
        ('FHD', _('Full HD (1080p)')),
        ('UHD', _('Ultra HD (4K)')),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('uz', _('Uzbek')),
        ('ru', _('Russian')),
        ('kr', _('Korean')),
        ('jp', _('Japanese')),
    ]
    
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name='videos',
        verbose_name=_('movie')
    )
    quality = models.CharField(_('quality'), max_length=10, choices=QUALITY_CHOICES, default='HD')
    language = models.CharField(_('language'), max_length=10, choices=LANGUAGE_CHOICES, default='en')
    subtitle_language = models.CharField(_('subtitle language'), max_length=10, choices=LANGUAGE_CHOICES, blank=True, null=True)
    
    video_file = models.FileField(_('video file'), upload_to='movies/videos/%Y/%m/%d/')
    thumbnail = models.ImageField(_('thumbnail'), upload_to='movies/thumbnails/%Y/%m/%d/', blank=True, null=True)
    
    size = models.BigIntegerField(_('size'), help_text=_("File size in bytes"), blank=True, null=True)
    duration = models.IntegerField(_('duration'), help_text=_("Duration in seconds"), blank=True, null=True)
    
    is_active = models.BooleanField(_('is active'), default=True)
    
    class Meta:
        db_table = 'videos'
        verbose_name = _('Video')
        verbose_name_plural = _('Videos')
        unique_together = ['movie', 'quality', 'language']
    
    def __str__(self):
        return f"{self.movie.title} - {self.quality} ({self.language})"
    
class MovieView(BaseModel):
    movie = models.ForeignKey(
        Movie, 
        on_delete=models.CASCADE, 
        related_name='views',
        verbose_name=_('movie')
    )
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name=_('user')
    )
    ip_address = models.GenericIPAddressField(_('ip address'))
    duration_watched = models.IntegerField(_('duration watched'), help_text=_("Seconds watched"), default=0)
    
    class Meta:
        db_table = 'movie_views'
        verbose_name = _('Movie View')
        verbose_name_plural = _('Movie Views')
    
    def __str__(self):
        return f"View: {self.movie.title}"

class Episode(BaseModel):
    tv_show = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='episodes',
        verbose_name=_('tv show'),
        limit_choices_to={'content_type': 'tv_show'}
    )
    season_number = models.PositiveIntegerField(_('season number'), default=1)
    episode_number = models.PositiveIntegerField(_('episode number'))
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'))
    duration = models.IntegerField(_('duration'), help_text=_("Duration in minutes"))
    
    class Meta:
        db_table = 'episodes'
        verbose_name = _('Episode')
        verbose_name_plural = _('Episodes')
        unique_together = ['tv_show', 'season_number', 'episode_number']
        ordering = ['season_number', 'episode_number']
    
    def __str__(self):
        return f"S{self.season_number:02d}E{self.episode_number:02d} - {self.title}"