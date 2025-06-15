from django.urls import path
from .views import ProtectedView

urlpatterns = [
    path("protected/", ProtectedView.as_view(), name="protected"),
]
