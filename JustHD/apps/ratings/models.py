from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.shared.models import BaseModel

class Rating(BaseModel):
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='ratings',
        verbose_name=_('user')
    )
    movie = models.ForeignKey(
        'movies.Movie', 
        on_delete=models.CASCADE, 
        related_name='ratings',
        verbose_name=_('movie')
    )
    score = models.PositiveSmallIntegerField(
        _('score'),
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text=_("Rating from 1 to 10")
    )
    comment = models.TextField(_('comment'), blank=True, null=True)

    class Meta:
        db_table = 'ratings'
        verbose_name = _('Rating')
        verbose_name_plural = _('Ratings')
        unique_together = ['user', 'movie']
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}: {self.score}/10"

    def save(self, *args, **kwargs):
        if self.score < 1:
            self.score = 1
        elif self.score > 10:
            self.score = 10
        super().save(*args, **kwargs)