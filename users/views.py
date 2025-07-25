from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework import generics, permissions, parsers
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    ChangePasswordSerializer,
    RequestOTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordWithOTPSerializer,
    LoginSerializer,
    RegisterSerializer,
    UserSrializers,


)
from .models import User
class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_description="Login to the application",
        responses={200: openapi.Response("Login successful"), 400: openapi.Response("Invalid id number or password")}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            reponse = {
                'token': token.key,
                'user_data': UserSrializers(serializer.validated_data.get('user')).data
            }
            return Response(reponse, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            token = data.get('token')
            response = {
                'token': token.key,
                'user_data': UserSrializers(data.get('user')).data
            }
            
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSrializers

    def get_object(self):
        return self.request.user
    
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer,tags=["Password reset"])
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data["old_password"]
        new_password = serializer.validated_data["new_password"]

        # Check if the old password is correct
        if not check_password(old_password, user.password):
            return Response(
                {"status": False, "message": "Old password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response(
            {"status": True, "message": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )
        

class RequestOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(request_body=RequestOTPSerializer,tags=["Password reset"])
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(request_body=VerifyOTPSerializer,tags=["Password reset"])
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ResetPasswordWithOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(request_body=ResetPasswordWithOTPSerializer,tags=["Password reset"])
    def post(self, request):
        serializer = ResetPasswordWithOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
