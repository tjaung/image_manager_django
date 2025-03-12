from rest_framework import serializers
from authentication.models import User  # Use the correct User model

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}  # Hide password from response
        }

    def create(self, validated_data):
        """Properly create a user with password hashing"""
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
