from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    )
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    UserSerializer,
    LoginSerializer,
    )

from .tokens import create_jwt_pair_for_user

User = get_user_model()


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=username, password=password)

            # Check if user is None (invalid credentials)
            if user is None:
                return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

            # Create JWT tokens for the authenticated user
            tokens = create_jwt_pair_for_user(user)

            # Return the tokens with a 200 OK status code
            return Response(
                {
                    **tokens,
                    "username": user.username,
                },
                status=status.HTTP_200_OK,
            )

        return Response(
                {"error": serializer.errors},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class SensitiveDataView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, *args, **kwargs):
        data = {"detail": "This is a secured endpoint for admins only"}

        return Response({
            **data
        },
        status=status.HTTP_200_OK)
