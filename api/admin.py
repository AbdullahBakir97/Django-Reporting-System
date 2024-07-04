from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from .models import User, MediaFile, Report

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
    list_display = ('username', 'first_name', 'last_name', 'full_name', 'email', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'full_name', 'email')
    ordering = ('username',)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = _('Full Name')


class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('user','file', 'uploaded_at')
    search_fields = ('user','file',)
    list_filter = ('uploaded_at',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'date_of_report', 'place_of_report')
    search_fields = ('user__username', 'description', 'place_of_report')
    list_filter = ('date_of_report',)

admin.site.register(User, UserAdmin)
admin.site.register(MediaFile, MediaFileAdmin)
admin.site.register(Report, ReportAdmin)

# Unregister the Group model to avoid conflict with your custom User model
admin.site.unregister(Group)
