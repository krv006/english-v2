from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import (
    UserListCreateAPIView, BooksViewSet, UnitsViewSet,
    AdminSiteSettingsListCreateAPIView, TestViewSet,
    VerifyEmailAPIView, RegisterAPIView, LoginAPIView
)

router = DefaultRouter()

app_name = 'apps'

router.register(r'books', BooksViewSet, basename='books')
router.register(r'units', UnitsViewSet, basename='units')
router.register(r'tests', TestViewSet, basename='tests')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserListCreateAPIView.as_view(), name='user-create'),
    path('admiVerificationCoden/', AdminSiteSettingsListCreateAPIView.as_view(), name='admin'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
]
