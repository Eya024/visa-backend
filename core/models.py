from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    passport_number = models.CharField(max_length=20)
    nationality = models.CharField(max_length=50)
    destination_country = models.CharField(max_length=50)
    visa_type = models.CharField(max_length=20)
    purpose_of_travel = models.CharField(max_length=255)
    duration_of_stay = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    education_level = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20)
    supporting_documents = models.TextField(blank=True)  # Comma-separated URLs
    additional_notes_file = models.FileField(upload_to='notes/', blank=True, null=True)
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
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_appointments', null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

class Availability(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='availabilities')
    day = models.CharField(max_length=20)
    time = models.CharField(max_length=20)



class PageVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100)
    visited_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} visited {self.page_name} at {self.visited_at}"
