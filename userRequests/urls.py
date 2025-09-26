from django.urls import path
from .views import ServiceRequestUpdateView, ServiceRequestListCreateView

urlpatterns = [
    path('requests/', ServiceRequestListCreateView.as_view(), name='service-request-list-create'),
    path('requests/<int:pk>/', ServiceRequestUpdateView.as_view(), name='service-request-update'),
]