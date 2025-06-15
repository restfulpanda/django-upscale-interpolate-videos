from django.urls import path

from .views import LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView

app_name = "authentication"
urlpatterns = [
    path("user", UserRetrieveUpdateAPIView.as_view(), name="get-user"),
    path("users/", RegistrationAPIView.as_view(), name="register"),
    path("users/login/", LoginAPIView.as_view(), name="login"),
]
