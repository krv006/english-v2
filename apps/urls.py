from django.urls import path

from apps.views import (
    RegisterAPIView, VerifyEmailAPIView, LoginAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
]
