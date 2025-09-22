from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Handles serialization and deserialization of User objects,
    including custom password handling for secure storage.
    """
    class Meta:
        """
        Meta class for UserSerializer.
        Specifies the model and fields to be serialized.
        Sets password as write-only for security.
        """
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new User instance, setting the password properly.
        Args:
            validated_data (dict): Validated data for creating the user.
        Returns:
            User: The created User instance with a hashed password.
        """
        password=validated_data.pop('password')
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user