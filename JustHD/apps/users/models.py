from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.shared.models import BaseModel

class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    bio = models.TextField(_('bio'), blank=True, null=True, max_length=500)
    
    is_premium = models.BooleanField(_('is premium'), default=False)
    premium_until = models.DateTimeField(_('premium until'), blank=True, null=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def has_active_premium(self):
        if not self.is_premium:
            return False
        if self.premium_until:
            from django.utils import timezone
            return timezone.now() < self.premium_until
        return self.is_premium

class UserProfile(BaseModel):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    language = models.CharField(
        _('language'),
        max_length=10, 
        choices=[
            ('en', _('English')),
            ('uz', _('Uzbek')),
            ('ru', _('Russian')),
        ],
        default='en'
    )
    theme = models.CharField(
        _('theme'),
        max_length=10,
        choices=[
            ('light', _('Light')),
            ('dark', _('Dark')),
        ],
        default='light'
    )
    notifications_enabled = models.BooleanField(_('notifications enabled'), default=True)
    email_notifications = models.BooleanField(_('email notifications'), default=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def has_active_premium(self):
        """Get premium status from related User model"""
        return self.user.has_active_premium