from celery.result import AsyncResult
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class VideoStatusView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get("task_id")
        result = AsyncResult(task_id)
        return Response(
            {"task_id": task_id, "status": result.status, "result": result.result}
        )
