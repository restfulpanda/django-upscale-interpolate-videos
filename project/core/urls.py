from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter

from logic.views import VideoViewSet
from tasks.views import get_status, home, run_task

schema_view = get_schema_view(
    openapi.Info(
        title="Video Processing API",
        default_version='v1',
    ),
    public=True,
)

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='upload_video')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/<task_id>/", get_status, name="get_status"),
    path("tasks/", run_task, name="run_task"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('videos/', include(router.urls)),
    path("", home, name="home"),
]
