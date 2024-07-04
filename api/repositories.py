from .models import MediaFile, Report
from django.contrib.auth import get_user_model

User = get_user_model()

# User operations
def get_all_users():
    return User.objects.all()

def get_user_by_id(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None
    
def get_user_by_email(email):
    return User.objects.filter(email=email).first()

def create_user(data):
    return User.objects.create(**data)

# MediaFile operations
def create_media_file(file):
    return MediaFile.objects.create(file=file)

def get_media_files_by_user(user):
    return MediaFile.objects.filter(user=user)

def get_media_file_by_id(file_id):
    try:
        return MediaFile.objects.get(id=file_id)
    except MediaFile.DoesNotExist:
        return None

def update_media_file(file_obj, new_file):
    file_obj.file = new_file
    file_obj.save()
    return file_obj

def delete_media_file(file_obj):
    file_obj.delete()

# Report operations
def create_report(user, description, place_of_report, files):
    report = Report.objects.create(user=user, description=description, place_of_report=place_of_report)
    for file in files:
        report.files.add(file)
    return report

def get_all_reports():
    return Report.objects.all()

def get_reports_by_user(user):
    return Report.objects.filter(user=user)

def get_report_by_id(report_id):
    try:
        return Report.objects.get(id=report_id)
    except Report.DoesNotExist:
        return None

def update_report(report_obj, description, place_of_report, files):
    report_obj.description = description
    report_obj.place_of_report = place_of_report
    report_obj.files.set(files)
    report_obj.save()
    return report_obj

def delete_report(report_obj):
    report_obj.delete()
