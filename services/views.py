from rest_framework.response import Response
from rest_framework import generics,permissions
from rest_framework.permissions import IsAuthenticated
from .models import Plan, Subscription
from .serializers import PlanSerializer, SubscriptionSerializer
from django.core.cache import cache
import logging

logger= logging.getLogger('django')

class PlanListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create telecom plans.
    - GET: Returns a cached list of all plans. If not cached, queries the database and caches the result for 5 minutes.
    - POST: Creates a new plan using PlanSerializer.
    """
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to retrieve all plans.
        Checks cache for 'plans_list'. If not found, queries the database,
        caches the result, and returns the list of plans.
        """
        logger.info("Fetching plans list from redis cache")
        cached_plans = cache.get('plans_list')
        if not cached_plans:
            logger.info("Cache miss - querying database for plans")
            cached_plans=list(self.get_queryset().values())
            cache.set('plans_list', cached_plans, timeout=300)  # Cache for 5 minutes
        return Response(cached_plans)
    
class SubscriptionCreateView(generics.CreateAPIView):
    """
    API view to create a new subscription for a telecom plan.
    Requires authentication.
    - POST: Creates a new subscription for the authenticated user using SubscriptionSerializer.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Called after serializer validation to save the subscription.
        Associates the subscription with the currently authenticated user.
        """
        logger.info(f"Creating subscription for user {self.request.user.username}")
        serializer.save(user=self.request.user)
