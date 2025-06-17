from django.urls import path
from .views import VideoUploadAPIView, VideoDownloadAPIView

app_name = "process-videos"
urlpatterns = [
    path("upload/", VideoUploadAPIView.as_view(), name="process-video"),
    path("download/<video_id>", VideoDownloadAPIView.as_view(), name="download-video"),
]
