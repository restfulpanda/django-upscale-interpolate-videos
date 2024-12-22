from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from .serializers import VideoSerializer
from tasks.sample_tasks import process_video

class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        video = serializer.save()
        task = process_video.delay(video.id)
        
        return Response(
            {"video_id": video.id, "task_id": task.id, "status": "Task submitted"},
            status=status.HTTP_202_ACCEPTED,
        )
