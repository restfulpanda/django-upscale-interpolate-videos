from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

app_name = "authentication"
urlpatterns = [
    path("user/", UserRetrieveUpdateAPIView.as_view(), name="get-user"),
    path("register/", RegistrationAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
