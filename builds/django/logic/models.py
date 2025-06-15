from django.db import models
from django.conf import settings
import os


def original_video_directory_path(instance, filename):
    return os.path.join("original", filename)


def processed_video_directory_path(instance, filename):
    return os.path.join("processed", filename)


class Video(models.Model):
    STATUS_TYPE_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("done", "Done"),
        ("failed", "Failed"),
    ]
    original_video = models.FileField(upload_to=original_video_directory_path)
    processed_video = models.FileField(
        upload_to=processed_video_directory_path, null=True, blank=True
    )

    status = models.CharField(
        max_length=20, choices=STATUS_TYPE_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
