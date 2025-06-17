import os

from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
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
        video = serializer.save(owner=self.request.user)
        task = process_video.delay(video.id)

        self.response_data = {
            "video_id": video.id,
            "task_id": task.id,
            "status": "Task submitted",
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.response_data, status=status.HTTP_202_ACCEPTED)


class VideoDownloadAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        video_id = kwargs.get("video_id")
        vid = get_object_or_404(Video, id=video_id)
        video_path = vid.processed_video.path

        if vid.owner != request.user:
            return Response({"detail": "Access denied."}, status=403)

        if os.path.exists(video_path):
            with open(video_path, "rb") as f:
                return FileResponse(f, content_type="video/mp4")

        raise Response({"detail": "File not found."}, status=404)
