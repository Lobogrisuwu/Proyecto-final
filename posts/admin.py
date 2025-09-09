from django.contrib import admin
from .models import Post, Like, Comment, Follow

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_at")
    list_filter = ("created_at",)
    search_fields = ("author__username", "caption")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__author__username", "text")

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "post", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__author__username")

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("id", "follower", "followed", "created_at")
    search_fields = ("follower__username", "followed__username")
