from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Video Processing API",
        default_version="v1",
        description="API for video processing",
    ),
    public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("users/", include("authentication.urls", namespace="authentication")),
    path("videos/", include("logic.urls", namespace="process_videos")),
    path("videos/", include("tasks.urls", namespace="tasks")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
