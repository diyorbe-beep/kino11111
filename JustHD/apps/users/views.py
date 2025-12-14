from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import User
from .serializers.auth import RegisterSerializer, LoginSerializer, ChangePasswordSerializer
from .serializers.profile import UserSerializer, UpdateProfileSerializer
from apps.shared.utils.custom_response import CustomResponse

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return CustomResponse.validation_error(
                    errors=serializer.errors,
                    request=request
                )
                
            user = serializer.save()
            
            # Profile should already be created by signal in serializer.save()
            # Just refresh to ensure we have the latest data
            user.refresh_from_db()
            
            refresh = RefreshToken.for_user(user)
            
            # Serialize user data safely
            try:
                user_data = UserSerializer(user, context={'request': request}).data
            except Exception as e:
                # If serialization fails, return basic user data
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'profile': None
                }
            
            return CustomResponse.success(
                message_key="CREATED",
                request=request,
                data={
                    'user': user_data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            )
        except Exception as e:
            # Log the error and return a generic error response
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Registration error: {str(e)}", exc_info=True)
            
            return CustomResponse.internal_error(
                request=request,
                context={'error': str(e)}
            )

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
            
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={
                'user': UserSerializer(user, context={'request': request}).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        logout(request)

        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={"message": "Successfully logged out"}
        )

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data=serializer.data
        )

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
            
        self.perform_update(serializer)
        
        return CustomResponse.success(
            message_key="UPDATED",
            request=request,
            data=UserSerializer(instance, context={'request': request}).data
        )

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return CustomResponse.validation_error(
                errors=serializer.errors,
                request=request
            )
            
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
     
        if not user.check_password(old_password):
            return CustomResponse.error(
                message_key="VALIDATION_ERROR",
                request=request,
                errors={"old_password": {
                    "en": "Current password is incorrect",
                    "uz": "Joriy parol noto'g'ri",
                    "ru": "Текущий пароль неверен"
                }}
            )

        user.set_password(new_password)
        user.save()

        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, user)
        
        return CustomResponse.success(
            message_key="SUCCESS_MESSAGE",
            request=request,
            data={"message": "Password changed successfully"}
        )

class TokenRefreshView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]

class CheckUsernameView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username', '').strip()
        if not username:
            return CustomResponse.validation_error(
                errors={"username": {
                    "en": "Username is required",
                    "uz": "Foydalanuvchi nomi talab qilinadi", 
                    "ru": "Имя пользователя обязательно"
                }},
                request=request
            )
        
        exists = User.objects.filter(username__iexact=username).exists()
        return CustomResponse.success(
            request=request,
            data={
                'username': username,
                'available': not exists
            }
        )

class CheckEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email', '').strip().lower()
        if not email:
            return CustomResponse.validation_error(
                errors={"email": {
                    "en": "Email is required",
                    "uz": "Email talab qilinadi",
                    "ru": "Email обязателен"
                }},
                request=request
            )
        
        exists = User.objects.filter(email__iexact=email).exists()
        return CustomResponse.success(
            request=request,
            data={
                'email': email,
                'available': not exists
            }
        )