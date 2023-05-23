from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.models import User

# Import Model
from cms_api.models import Post, Like


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class PostSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "content",
            "created",
            "is_public",
            "owner",
            "like_count",
        ]
        read_only_fields = ["like_count"]
        extra_kwargs = {"owner": {"required": False}}

    def create(self, validated_data):
        # Set the owner of the user to the authenticated user
        validated_data["owner"] = self.context["user"]
        return super().create(validated_data)

    def get_like_count(self, obj):
        return obj.like_set.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "user", "created"]
        extra_kwargs = {"user": {"required": False}}

    def validate(self, attrs):
        user = self.context["user"]
        post = attrs["post"]

        # Check if a like already exists for the user and post combination
        if Like.objects.filter(user=user, post=post).exists():
            raise ValidationError("A like already exists for this user and post.")

        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        return super().create(validated_data)
