### videos/models.py

from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    
    def increment_views(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} - {self.video.title}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.video.title}"
    
class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_seconds = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'video')
    
    @property
    def progress_percentage(self):
        if self.video.duration:
            return min(round((self.watched_seconds / self.video.duration.total_seconds()) * 100, 100))
        return 0