from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.shared.models import BaseModel

class Comment(BaseModel):
    user = models.ForeignKey(
        'users.User', 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name=_('user')
    )
    movie = models.ForeignKey(
        'movies.Movie', 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name=_('movie')
    )
    text = models.TextField(_('text'))
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies',
        verbose_name=_('parent comment')
    )
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        db_table = 'comments'
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    @property
    def has_replies(self):
        return self.replies.filter(is_active=True).exists()