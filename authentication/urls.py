from django.urls import path

from authentication.views import (
    CreateUserView,
    UserLoginView,
)


urlpatterns = [
    path("users/", CreateUserView.as_view()),
    path("login/", UserLoginView.as_view()),
]
