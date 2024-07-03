from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, MediaFile
from .serializers import UserSerializer, MediaFileSerializer
import random

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OTPLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()
        send_mail('Your OTP Code', f'Your OTP code is {otp}', 'from@example.com', [email])
        return Response({'message': 'OTP sent'})

    def put(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = get_object_or_404(User, email=email, otp=otp)
        user.otp = ''
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

class MediaFileView(generics.ListCreateAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MediaFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
