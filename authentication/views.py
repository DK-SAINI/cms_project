from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.views.generic import TemplateView

# import serializer
from authentication.serializer import UserRegisterSerializer, UserLoginSerializer


class CreateUserView(APIView):
    def post(self, request):
        # Passing our data in the seriealizer
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "User Registered Successfully",
                    "data": None,
                },
                status=status.HTTP_201_CREATED,
            )

        # All serializer error stores in errors
        response = {"status": False, "errors": serializer.errors, "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            # genrate new token
            token, created = Token.objects.get_or_create(user=user)

            # Success Response
            return Response(
                {
                    "status": True,
                    "message": "Login Successfully",
                    "data": {"token": token.key},
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
