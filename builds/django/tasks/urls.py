from django.urls import path

from .views import VideoStatusView

app_name = "tasks"
urlpatterns = [
    path("<task_id>/status/", VideoStatusView.as_view(), name="get-video-status"),
]
