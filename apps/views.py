import random
import string

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User
from apps.serializers import (
    LoginSerializer,
    LoginUserModelSerializer,
    RegisterSerializer,
)
from apps.task import send_verification_email


@extend_schema(tags=['users'])
class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    # Register a new user
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate a random 6-digit verification code
            verification_code = ''.join(random.choices(string.digits, k=6))
            user.reset_token = verification_code
            user.save()

            # Send the email asynchronously with Celery
            send_verification_email.delay(user.email, verification_code)

            return Response({"message": "User registered successfully. Check your email for the verification code."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.response import Response


@extend_schema(tags=['users'])
class VerifyEmailAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request):
        # print("Request data:", request.data)  # Debugging the incoming data
        email = request.data.get('email')
        verification_code = request.data.get('verification_code') or request.data.get('password')  # Temporary fix

        # print("Request data:", request.data)  # This should now include 'verification_code'
        # print("Verification Code:", request.data.get('verification_code'))

        if not email or not verification_code:
            return Response({"error": "Email and verification code are required."}, status=400)

        try:
            user = User.objects.get(email=email, reset_token=verification_code)
            user.is_active = True
            user.reset_token = ''
            user.save()
            return Response({"message": "Email verified successfully."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or verification code."}, status=400)


@extend_schema(tags=['users'])
class LoginAPIView(GenericAPIView):
    permission_classes = AllowAny,
    authentication_classes = ()

    def get_serializer_class(self):
        return LoginUserModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
