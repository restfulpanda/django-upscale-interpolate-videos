from django.urls import path

from .views import VideoStatusView

app_name = "tasks"
urlpatterns = [
    path("status/<task_id>", VideoStatusView.as_view(), name="get-video-status"),
]
