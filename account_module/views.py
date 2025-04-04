from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = request.data.get("phone_number")
            password = request.data.get("password")
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({
                    "error": "phone number is already registered."
                })
            serializer.save(phone_number=phone_number, password=password)
            return Response({
                "message": "User signed up successfully."
            })
        return Response({
            "error": "Invalid phone number or password."
        })
    
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
class UserLoginView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = User.objects.get(phone_number=phone_number, password=password)
        if user:
            return Response({
                'message': 'Login successful.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid phone number or password.'}, status=status.HTTP_401_UNAUTHORIZED)
