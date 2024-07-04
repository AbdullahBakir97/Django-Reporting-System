from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
import random
from .repositories import *
from .serializers import UserSerializer, MediaFileSerializer, ReportSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        create_user(serializer.validated_data)

class OTPLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        user = get_user_by_email(email)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()
        send_mail('Your OTP Code', f'Your OTP code is {otp}', 'from@example.com', [email])
        return Response({'message': 'OTP sent'})

    def put(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        user = get_user_by_email(email)
        if not user or user.otp != otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user.otp = ''
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

class MediaFileView(generics.ListCreateAPIView):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_media_files_by_user(self.request.user)

    def perform_create(self, serializer):
        create_media_file(file=serializer.validated_data['file'])

class MediaFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MediaFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_media_files_by_user(self.request.user)

    def perform_update(self, serializer):
        media_file = get_media_file_by_id(self.kwargs['pk'])
        if media_file:
            update_media_file(media_file, serializer.validated_data['file'])

    def perform_destroy(self, instance):
        delete_media_file(instance)

class ReportView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_reports_by_user(self.request.user)

    def perform_create(self, serializer):
        files_data = self.request.FILES.getlist('files')
        media_files = [create_media_file(file) for file in files_data]
        create_report(
            user=self.request.user,
            description=serializer.validated_data['description'],
            place_of_report=serializer.validated_data['place_of_report'],
            files=media_files
        )

class ReportDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_reports_by_user(self.request.user)

    def perform_update(self, serializer):
        report = get_report_by_id(self.kwargs['pk'])
        if report:
            files_data = self.request.FILES.getlist('files')
            media_files = [create_media_file(file) for file in files_data]
            update_report(
                report,
                description=serializer.validated_data['description'],
                place_of_report=serializer.validated_data['place_of_report'],
                files=media_files
            )

    def perform_destroy(self, instance):
        delete_report(instance)
