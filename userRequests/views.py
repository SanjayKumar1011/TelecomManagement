from django.shortcuts import render
from rest_framework import generics, permissions
from .models import ServiceRequest
from .serializers import UserRequestSerializer  
import logging
from rest_framework.response import Response

logger = logging.getLogger('django')

class ServiceRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = UserRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Returns the queryset of ServiceRequest objects for the authenticated user.
        """
        user = self.request.user
        logger.info(f"Fetching service requests for user {user.username}")
        if user=="Customer":
            return ServiceRequest.objects.filter(customer=user)
        return ServiceRequest.objects.all()
    def perform_create(self, serializer):
        """
        Called after serializer validation to save the service request.
        Associates the service request with the currently authenticated user as the customer.
        """
        user = self.request.user
        logger.info(f"Creating service request for user {user.username}")
        serializer.save(customer=user)

class ServiceRequestUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing service request.
    Only users with 'Admin' or 'Support' roles are allowed to update service requests.
    """
    queryset = ServiceRequest.objects.all()
    serializer_class = UserRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.role.lower() not in ["admin", "support"]:
            logger.warning(f"User {request.user.username} attempted but the user has role {request.user.role}")
            logger.warning(f"User {request.user.username} attempted to update service request without permission")
            return Response({"detail": "Only Admin or Support can Update"}, status=403)
        return super().update(request, *args, **kwargs)