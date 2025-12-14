from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.users.models import User

class MultiFieldBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            user = User.objects.get(
                Q(username=username) | 
                Q(email=username) | 
                Q(phone=username)
            )
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(
                Q(username=username) | 
                Q(email=username) | 
                Q(phone=username)
            ).first()
        
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None