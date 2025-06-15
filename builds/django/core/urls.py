from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.routers import DefaultRouter

from tasks.views import get_video_status

schema_view = get_schema_view(
    openapi.Info(
        title="Video Processing API",
        default_version="v1",
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
    path("", include('apps.authentication.urls', namespace='authentication')),
    path("", include('apps.logic.urls', namespace='process_videos')),
    path("", include('apps.tasks.urls', namespace='tasks')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
