from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='api_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='api_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_of_report = models.DateTimeField(auto_now_add=True)
    place_of_report = models.CharField(max_length=255)
    files = models.ManyToManyField('MediaFile', blank=True)

class MediaFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
