from celery.result import AsyncResult
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def get_video_status(request, task_id):
    result = AsyncResult(task_id)
    return Response(
        {"task_id": task_id, "status": result.status, "result": result.result}
    )
