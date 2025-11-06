# core/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Extend User with Profile (for premium status)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {'Premium' if self.is_premium else 'Free'}"

# Academic Year (1 to 4)
class AcademicYear(models.Model):
    year_number = models.IntegerField(unique=True, choices=[
        (1, 'Year 1'),
        (2, 'Year 2'),
        (3, 'Year 3'),
        (4, 'Year 4'),
    ])

    class Meta:
        ordering = ['year_number']
        verbose_name_plural = "Academic Years"

    def __str__(self):
        return f"Year {self.year_number}"

# Semester (1 or 2) within a year
class Semester(models.Model):
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
    ]
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.IntegerField(choices=SEMESTER_CHOICES)

    class Meta:
        ordering = ['year__year_number', 'semester_number']
        unique_together = ('year', 'semester_number')

    def __str__(self):
        return f"Year {self.year.year_number}, Semester {self.semester_number}"

# Exam Type (MST1, MST2, EST)
class ExamType(models.Model):
    name = models.CharField(max_length=10, unique=True, choices=[
        ('MST1', 'Mid Semester Test 1'),
        ('MST2', 'Mid Semester Test 2'),
        ('EST', 'End Semester Test'),
    ])

    def __str__(self):
        return self.name

# Resource: The core content (PYQs, videos, sheets, etc.)
class Resource(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='resources')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='resources')
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    book_recommendation = models.CharField(max_length=200, blank=True, help_text="e.g., 'Computer Organization by Hamacher'")
    book_pages = models.CharField(max_length=100, blank=True, help_text="e.g., 'pp. 45–67'")
    
    video_url = models.URLField(blank=True, help_text="YouTube embed link (e.g., https://www.youtube.com/embed/abc123)")
    
    practice_sheet = models.FileField(upload_to='practice_sheets/', blank=True, null=True)
    pyq_pdf = models.FileField(upload_to='pyqs/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_premium = models.BooleanField(default=True, help_text="Only premium users can access this")

    class Meta:
        ordering = ['semester__year__year_number', 'semester__semester_number', 'exam_type']

    def __str__(self):
        return f"{self.title} ({self.semester} - {self.exam_type})"

    def get_absolute_url(self):
        return reverse('resource_detail', kwargs={
            'year_num': self.semester.year.year_number,
            'sem_num': self.semester.semester_number,
            'exam_name': self.exam_type.name.lower(),
        })
