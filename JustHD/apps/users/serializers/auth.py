from rest_framework import serializers
from django.contrib.auth import authenticate
from apps.users.models import User, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone'
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        
        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": {
                    "en": "Passwords do not match.",
                    "uz": "Parollar mos kelmadi.",
                    "ru": "Пароли не совпадают."
                }
            })
        
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "email": {
                    "en": "A user with this email already exists.",
                    "uz": "Bu email bilan foydalanuvchi allaqachon mavjud.",
                    "ru": "Пользователь с этим email уже существует."
                }
            })
        
        username = attrs.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "username": {
                    "en": "A user with this username already exists.",
                    "uz": "Bu foydalanuvchi nomi bilan allaqachon mavjud.",
                    "ru": "Пользователь с этим именем уже существует."
                }
            })
        
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        # Profile should be created by signal, but ensure it exists
        # Refresh from DB to get the profile created by signal
        user.refresh_from_db()
        
        # Double-check profile exists
        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # If profile doesn't exist, create it
            UserProfile.objects.create(user=user)
            user.refresh_from_db()
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError({
                    "non_field_errors": {
                        "en": "Invalid credentials",
                        "uz": "Noto'g'ri ma'lumotlar",
                        "ru": "Неверные учетные данные"
                    }
                })
            if not user.is_active:
                raise serializers.ValidationError({
                    "non_field_errors": {
                        "en": "User account is disabled",
                        "uz": "Foydalanuvchi hisobi o'chirilgan",
                        "ru": "Учетная запись пользователя отключена"
                    }
                })
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError({
            "non_field_errors": {
                "en": 'Must include "username" and "password"',
                "uz": '"Foydalanuvchi nomi" va "parol" kiritilishi shart',
                "ru": 'Необходимо указать "имя пользователя" и "пароль"'
            }
        })

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        
        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                "new_password_confirm": {
                    "en": "New passwords do not match.",
                    "uz": "Yangi parollar mos kelmadi.",
                    "ru": "Новые пароли не совпадают."
                }
            })
        return attrs