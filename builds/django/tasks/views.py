from celery.result import AsyncResult
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class VideoStatusView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, task_id, *args, **kwargs):
        result = AsyncResult(task_id)
        return Response({
            "task_id": task_id,
            "status": result.status,
            "result": result.result
        })