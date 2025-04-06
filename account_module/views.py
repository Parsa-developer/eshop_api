from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserSerializer, UserRegisterSerializer, UserLoginSerializer
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout, authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
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
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid:
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')

            user = User.objects.get(phone_number=phone_number)
            if user:
                if user.check_password(password):
                    login(request, user)
                    return Response({
                        'message': 'Login successful.'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Invalid information'
                    })
            else:
                return Response({'error': 'Invalid phone number or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Invalid information'
            })

class UserLogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logout(request)
        return Response({
            'success': 'You logged out!'
        })
    
class CheckAuthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "is_authenticated": True,
            "user": str(request.user)  # Or serialize user data
        })