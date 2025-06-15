from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter

from logic.views import VideoViewSet
from tasks.views import get_video_status

schema_view = get_schema_view(
    openapi.Info(
        title="Video Processing API",
        default_version="v1",
    ),
    public=True,
)

router = DefaultRouter()
router.register(r"videos", VideoViewSet, basename="upload_video")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/<task_id>/status/", get_video_status, name="get_video_status"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
