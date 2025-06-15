from django.urls import path

from .views import get_video_status

app_name = 'tasks'
urlpatterns = [
    path("tasks/<task_id>/status/", get_video_status, name="get_video_status"),
]