import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.mark.django_db
def test_video_upload():
    client = APIClient()
    video_file = SimpleUploadedFile("test.mp4", b"file_content", content_type="video/mp4")
    response = client.post('/api/videos/', {'original_video': video_file})
    assert response.status_code == 201