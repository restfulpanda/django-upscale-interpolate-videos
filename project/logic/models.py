from django.db import models

class Video(models.Model):
    original_video = models.FileField(upload_to='original/')
    processed_video = models.FileField(upload_to='processed/', null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, done, failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
