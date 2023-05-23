from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# Import Model and Serializer
from cms_api.models import Post, Like
from cms_api.serializer import UserSerializer, PostSerializer, LikeSerializer


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        if user_id is not None:
            user = get_object_or_404(User, id=user_id)
            serializer = UserSerializer(user)
            return Response(
                {
                    "status": True,
                    "message": "User Information",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(
                {
                    "status": True,
                    "message": "All User Information",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if user != request.user:
            return Response(
                {
                    "status": False,
                    "error": "You do not have permission to update this user.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "User detail update successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if user != request.user:
            return Response(
                {
                    "status": False,
                    "error": "You do not have permission to delete this user.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        user.delete()
        return Response(
            {
                "status": True,
                "error": "Your Account deleted successfully.",
                "data": None,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class PostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Create Post Successfully.",
                    "data": None,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, post_id=None):
        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)

            if post.is_public is False and post.owner != request.user:
                return Response(
                    {
                        "status": True,
                        "error": "You do not have permission to access this private post.",
                        "data": None,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = PostSerializer(post)
        else:
            if "owner" in request.query_params:
                # Filter posts by owner if owner parameter is present in query params
                posts = Post.objects.filter(owner=request.user, is_public=False)

            else:
                # Retrieve all posts if owner parameter is not present
                posts = Post.objects.filter(is_public=True)

            serializer = PostSerializer(posts, many=True)

        return Response(
            {
                "status": True,
                "message": "Posts Data",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.owner != request.user:
            return Response(
                {
                    "status": False,
                    "error": "You do not have permission to Update this Post.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Update Post Successfully.",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.owner != request.user:
            return Response(
                {
                    "status": False,
                    "error": "You do not have permission to delete this Post.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        post.delete()
        return Response(
            {
                "status": True,
                "message": "Your Post deleted successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LikeSerializer(data=request.data, context={"user": request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Add Like Successfully.",
                    "data": None,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, like_id=None):
        if like_id is not None:
            like = get_object_or_404(Like, id=like_id)
            serializer = LikeSerializer(like)
            return Response(serializer.data)
        else:
            likes = Like.objects.all()
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)

    def put(self, request, like_id):
        like = Like.objects.get(id=like_id)

        if like.user != request.user:
            return Response(
                {
                    "status": False,
                    "error": "You do not have permission to Update this Like.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = LikeSerializer(like, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": True,
                    "error": "Update Successfully.",
                    "data": serializer.data,
                },
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, like_id):
        like = get_object_or_404(Like, id=like_id)

        if like.user != request.user:
            return Response(
                {
                    "status": False,
                    "error": "You do not have permission to delete this Like.",
                    "data": None,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        like.delete()
        return Response(
            {
                "status": True,
                "message": "Your Like deleted successfully.",
                "data": None,
            },
            status=status.HTTP_200_OK,
        )
