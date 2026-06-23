from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_documents')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Workflow Nodes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    manager_remarks = models.TextField(blank=True, null=True)

    # AI Metadata Extracts
    ai_summary = models.TextField(blank=True, null=True)
    ai_category = models.CharField(max_length=100, blank=True, null=True)
    ai_priority = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title