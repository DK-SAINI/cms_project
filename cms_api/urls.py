from django.urls import path
from .views import UserAPIView, PostAPIView, LikeAPIView

urlpatterns = [
    path("user_details/", UserAPIView.as_view()),
    path("user_details/<int:user_id>/", UserAPIView.as_view()),
    path("posts/", PostAPIView.as_view()),
    path("posts/<int:post_id>/", PostAPIView.as_view()),
    path("likes/", LikeAPIView.as_view()),
    path("likes/<int:like_id>/", LikeAPIView.as_view()),
]
