from rest_framework import serializers
from .models import ServiceRequest 


class UserRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserRequest model.
    Handles serialization and deserialization of UserRequest objects.
    """
    class Meta:
        """
        Meta class for UserRequestSerializer.
        Specifies the model and fields to be serialized.
        """
        model = ServiceRequest
        fields = "__all__"
        read_only_fields = ["customer", "created_at", "resolved_at"]