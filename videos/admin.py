### videos/admin.py
from django.contrib import admin
from .models import Video, Bookmark, Comment
from .models import VideoProgress

admin.site.register(VideoProgress)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    list_filter = ('course__topic', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    ordering = ('course', 'order')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'video__title')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'video__title', 'content')
    ordering = ('-created_at',)