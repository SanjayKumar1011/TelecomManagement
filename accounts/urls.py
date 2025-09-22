from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import RegisterView

urlpatterns = [
    # Endpoint for user registration
    path("register/", RegisterView.as_view(), name="register"),

    # Endpoint for login, returns JWT access and refresh tokens
    path("login/", TokenObtainPairView.as_view(), name="login"),

    # Endpoint for refreshing expired tokens
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]