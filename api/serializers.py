from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MediaFile, Report

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'date_of_birth', 'place_of_birth', 'gender', 'address', 'national_id']

class MediaFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ['id', 'user', 'file', 'uploaded_at']

class ReportSerializer(serializers.ModelSerializer):
    files = MediaFileSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'user', 'description', 'date_of_report', 'place_of_report', 'files']
