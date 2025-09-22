from .serializers import UserSerializer
from rest_framework import generics
from .models import User
import logging
# Create your views here.

class RegisterView(generics.CreateAPIView):
    """
    API view to register a new user.
    Uses UserSerializer to validate and create the user instance.
    If perform_create is not defined, the default implementation will call
    serializer.save(), which invokes the serializer's create() method.
    Override perform_create if you need to add custom actions (e.g., logging)
    after the user is created.
    """
    logger= logging.getLogger('django')
   
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Called after the serializer's create() method.
        Used here to log user registration events.
        """
        user = serializer.save()
        self.logger.info(f"User {user.username} registered successfully with role {user.role}")
