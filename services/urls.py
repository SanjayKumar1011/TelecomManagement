from django.urls import path
from .views import PlanListCreateView, SubscriptionCreateView

urlpatterns = [
    path("plans/", PlanListCreateView.as_view(), name="plans"),
    path("subscribe/", SubscriptionCreateView.as_view(), name="subscribe"),
]
