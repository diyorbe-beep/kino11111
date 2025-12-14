from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

def superuser_required(
        view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="admin:login"
):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def premium_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from rest_framework.exceptions import NotAuthenticated
            raise NotAuthenticated("Authentication required")

        if not hasattr(request.user, 'has_active_premium') or not request.user.has_active_premium:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Premium subscription required")
            
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def staff_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="admin:login"):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator