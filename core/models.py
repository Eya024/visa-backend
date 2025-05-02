from django.db import models
from django.contrib.auth.models import AbstractUser

# User model with roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('advisor', 'Advisor'),
    ]
    role = models.CharField(max_length=20, default='student')

    phone_number = models.CharField(max_length=20, blank=True)

class Application(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Document(models.Model):
    DOC_TYPES = [
        ('passport', 'Passport'),
        ('transcript', 'Transcript'),
        ('ielts', 'IELTS'),
        ('bank_statement', 'Bank Statement'),
    ]
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, choices=DOC_TYPES)
    file_url = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_appointments')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_appointments')
    date = models.DateTimeField()
    meeting_link = models.TextField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled')
