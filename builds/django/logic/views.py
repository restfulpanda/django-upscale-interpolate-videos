from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Video
from .serializers import VideoSerializer
from tasks.sample_tasks import process_video


class VideoUploadAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        video = serializer.save()
        task = process_video.delay(video.id)

        self.response_data = {
            "video_id": video.id,
            "task_id": task.id,
            "status": "Task submitted",
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.response_data, status=status.HTTP_202_ACCEPTED)
