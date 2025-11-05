# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import AcademicYear, Semester, ExamType, Resource, Profile

# Inline Profile in User admin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['year_number']
    ordering = ['year_number']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['year', 'semester_number']
    list_filter = ['year']

@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'semester', 'exam_type', 'is_premium']
    list_filter = ['semester__year', 'exam_type', 'is_premium']
    search_fields = ['title', 'description']