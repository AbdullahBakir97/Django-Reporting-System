from django.urls import path
from .views import RegisterView, OTPLoginView, MediaFileView, MediaFileDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('otp-login/', OTPLoginView.as_view(), name='otp-login'),
    path('media/', MediaFileView.as_view(), name='media-list'),
    path('media/<int:pk>/', MediaFileDetailView.as_view(), name='media-detail'),
]
