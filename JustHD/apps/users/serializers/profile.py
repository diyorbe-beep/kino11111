from rest_framework import serializers
from apps.users.models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('language', 'theme', 'notifications_enabled', 'email_notifications')
        read_only_fields = ('id',)

class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    full_name = serializers.ReadOnlyField()
    has_active_premium = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone', 'avatar', 'date_of_birth', 'bio',
            'is_premium', 'has_active_premium', 'premium_until',
            'profile', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_premium', 'premium_until')
    
    def get_profile(self, obj):
        """Safely get profile, return None if doesn't exist"""
        try:
            # Use getattr with default to avoid DoesNotExist exception
            profile = getattr(obj, 'profile', None)
            if profile:
                return UserProfileSerializer(profile).data
        except Exception:
            # Catch any exception and return None
            pass
        return None

class UpdateProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'phone', 
            'avatar', 'date_of_birth', 'bio', 'profile'
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance