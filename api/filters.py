import django_filters
from .models import User, Report, MediaFile
from .repositories import get_all_reports, get_reports_by_user, get_all_users, get_media_files_by_user

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'email']

class ReportFilter(django_filters.FilterSet):
    class Meta:
        model = Report
        fields = ['user', 'date_of_report']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['user'].queryset = get_all_users()

class MediaFileFilter(django_filters.FilterSet):
    class Meta:
        model = MediaFile
        fields = ['user', 'uploaded_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['user'].queryset = get_all_users()
