from django.contrib import admin
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, MediaFile, Report
from .repositories import *
from django.urls import path
from .filters import UserFilter, ReportFilter, MediaFileFilter

# Placeholder for MediaFileInline
class MediaFileInline(admin.TabularInline):
    model = MediaFile
    extra = 0

class ReportInline(admin.TabularInline):
    model = Report
    extra = 0

class CustomAdminSite(admin.AdminSite):
    site_header = 'Custom Admin Dashboard'
    site_title = 'Admin Portal'
    index_title = 'Welcome to the Admin Dashboard'

    def index(self, request, extra_context=None):
        user_filter = UserFilter(request.GET, queryset=get_all_users())
        report_filter = ReportFilter(request.GET, queryset=get_all_reports())
        mediafile_filter = MediaFileFilter(request.GET, queryset=get_media_files_by_user(request.user))

        context = dict(
            self.each_context(request),
            user_count=User.objects.count(),
            mediafile_count=MediaFile.objects.count(),
            report_count=Report.objects.count(),
            users=user_filter.qs,
            mediafiles=mediafile_filter.qs,
            reports=report_filter.qs,
            user_filter=user_filter,
            report_filter=report_filter,
            mediafile_filter=mediafile_filter,
        )
        return render(request, 'admin/custom_dashboard.html', context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('create_user/', self.admin_view(self.create_user_view), name='custom_admin_create_user'),
            path('create_mediafile/', self.admin_view(self.create_mediafile_view), name='custom_admin_create_mediafile'),
            path('create_report/', self.admin_view(self.create_report_view), name='custom_admin_create_report'),
        ]
        return custom_urls + urls

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def create_user_view(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            user = create_user({'username': username, 'email': email})
            return redirect('custom_admin:index')

    def create_mediafile_view(self, request):
        if request.method == 'POST':
            user_id = request.POST['user']
            file = request.FILES['file']
            user = get_user_by_id(user_id)
            mediafile = create_media_file({'user': user, 'file': file})
            return redirect('custom_admin:index')

    def create_report_view(self, request):
        if request.method == 'POST':
            user_id = request.POST['user']
            description = request.POST['description']
            place_of_report = request.POST['place_of_report']
            user = get_user_by_id(user_id)
            report = create_report(user, description, place_of_report, [])
            return redirect('custom_admin:index')
    
    def get_key_metrics(self):
        # Implement logic to get key metrics
        return {}
    
    def get_recent_activities(self):
        # Implement logic to get recent activities
        return []
    
    def get_important_notifications(self):
        # Implement logic to get important notifications
        return []

custom_admin_site = CustomAdminSite(name='custom_admin')

class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'full_name', 'email', 'date_of_birth', 'place_of_birth', 'gender', 'address', 'national_id')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional info'), {'fields': ('otp',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'full_name', 'email', 'is_staff', 'get_report_count', 'get_media_files')
    search_fields = ('username', 'first_name', 'last_name', 'full_name', 'email', 'address', 'national_id')
    ordering = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = _('Full Name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile').prefetch_related('report_set', 'mediafile_set')

    def get_report_count(self, obj):
        return obj.report_set.count()
    get_report_count.short_description = _('Report Count')

    def get_media_files(self, obj):
        return ", ".join([file.file.name for file in obj.mediafile_set.all()])
    get_media_files.short_description = _('Media Files')

    def changelist_view(self, request, extra_context=None):
        context = dict(
            self.admin_site.each_context(request),
            key_metrics=self.get_key_metrics(),
            recent_activities=self.get_recent_activities(),
        )
        return super().changelist_view(request, extra_context=context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = dict(
            self.admin_site.each_context(request),
            additional_info=self.get_additional_info(object_id),
        )
        return super().change_view(request, object_id, form_url, extra_context=context)

    def get_additional_info(self, object_id):
        # Implement logic to get additional information
        return {}

    def get_inline_instances(self, request, obj=None):
        return [MediaFileInline(self.model, self.admin_site), ReportInline(self.model, self.admin_site)]

    actions = ['export_csv', 'send_notification']

    def export_csv(self, request, queryset):
        # Implement your export logic here
        self.message_user(request, "Selected users exported to CSV successfully.")
    export_csv.short_description = "Export selected users to CSV"

    def send_notification(self, request, queryset):
        # Implement your notification logic here
        self.message_user(request, "Notification sent to selected users.")
    send_notification.short_description = "Send notification to selected users"


class MediaFileAdmin(admin.ModelAdmin):
    model = MediaFile
    list_display = ('user', 'file_name', 'uploaded_at', 'get_reports_for_media_file')
    search_fields = ('user__username', 'file',)
    list_filter = ('uploaded_at',)

    def file_name(self, obj):
        return obj.file.name
    file_name.short_description = _('File Name')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

    def delete_model(self, request, obj):
        delete_media_file(obj)
        super().delete_model(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('report_set')

    def get_reports_for_media_file(self, obj):
        return ", ".join([str(report) for report in obj.report_set.all()])
    get_reports_for_media_file.short_description = _('Reports')


class ReportAdmin(admin.ModelAdmin):
    model = Report
    list_display = ('user', 'description', 'date_of_report', 'place_of_report', 'get_media_files')
    search_fields = ('user__username', 'description', 'place_of_report')
    list_filter = ('date_of_report',)

    def save_model(self, request, obj, form, change):
        if not change:
            files_data = request.FILES.getlist('files')
            media_files = [create_media_file(file) for file in files_data]
            create_report(
                user=request.user,
                description=form.cleaned_data['description'],
                place_of_report=form.cleaned_data['place_of_report'],
                files=media_files
            )
        else:
            files_data = request.FILES.getlist('files')
            media_files = [create_media_file(file) for file in files_data]
            update_report(
                obj,
                description=form.cleaned_data['description'],
                place_of_report=form.cleaned_data['place_of_report'],
                files=media_files
            )
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        delete_report(obj)
        super().delete_model(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user').prefetch_related('files')

    def get_media_files(self, obj):
        return ", ".join([file.file.name for file in obj.files.all()])
    get_media_files.short_description = _('Media Files')


custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(MediaFile, MediaFileAdmin)
custom_admin_site.register(Report, ReportAdmin)

# Unregister the Group model to avoid conflict with your custom User model
admin.site.unregister(Group)


custom_admin_site.register(Group)