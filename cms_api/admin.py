from django.contrib import admin
from cms_api.models import Post, Like

# Register your models here.


@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    model = Post

    list_display = (
        "id",
        "title",
        "description",
        "content",
        "owner",
        "is_public",
    )


@admin.register(Like)
class ProfileAdmin(admin.ModelAdmin):
    model = Like

    list_display = (
        "id",
        "user",
        "post",
    )
