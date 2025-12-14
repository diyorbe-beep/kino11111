from django.urls import path
from .. import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.LoginView.as_view(), name='login'),  # Changed from 'login/' to 'token/' for JWT compatibility
    path('login/', views.LoginView.as_view(), name='login-alt'),  # Keep for backward compatibility
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token-refresh'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    path('check-username/', views.CheckUsernameView.as_view(), name='check-username'),
    path('check-email/', views.CheckEmailView.as_view(), name='check-email'),
]