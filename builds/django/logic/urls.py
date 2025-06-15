from django.urls import path

from .views import VideoViewSet

app_name = 'process_videos'
urlpatterns = [
    path('process-video/', VideoViewSet.as_view()),
]