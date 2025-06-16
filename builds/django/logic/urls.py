from django.urls import path
from .views import VideoUploadAPIView

app_name = "process-videos"
urlpatterns = [
    path("upload/", VideoUploadAPIView.as_view(), name="process-video"),
]
