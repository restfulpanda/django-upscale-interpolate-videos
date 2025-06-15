from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoViewSet

router = DefaultRouter()
router.register(r'process-video', VideoViewSet, basename='video')

app_name = 'process_videos'

urlpatterns = [
    path('', include(router.urls)),
]