from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from authentication.models import User  # Use the correct User model

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model with password validation"""

    password = serializers.CharField(
        write_only=True, required=True, min_length=8
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'confirm_password': {'write_only': True, 'required': True},
        }

    def validate(self, data):
        """Custom validation for password strength and matching passwords"""
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # 1️⃣ Ensure passwords match
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        # 2️⃣ Validate password strength
        try:
            validate_password(password)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return data

    def create(self, validated_data):
        """Properly create a user with password hashing"""
        validated_data.pop("confirm_password")  # Remove confirm_password from validated data
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
