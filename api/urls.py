from django.urls import path
from .views import RegisterView, OTPLoginView, MediaFileView, MediaFileDetailView, ReportView, ReportDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('otp-login/', OTPLoginView.as_view(), name='otp_login'),
    path('media/', MediaFileView.as_view(), name='media_list_create'),
    path('media/<int:pk>/', MediaFileDetailView.as_view(), name='media_detail'),
    path('reports/', ReportView.as_view(), name='report_list_create'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),
]
