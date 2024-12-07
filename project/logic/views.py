from rest_framework.viewsets import ModelViewSet
from .models import Video
from .serializers import VideoSerializer
from tasks.sample_tasks import process_video

class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        video = serializer.save()
        process_video.delay(video.id)
