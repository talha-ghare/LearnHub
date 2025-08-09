from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse

User = get_user_model()

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topic_detail', kwargs={'slug': self.slug})

class Course(models.Model):
    view_count = models.PositiveIntegerField(default=0)
    
    def increment_views(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def get_total_duration(self):
        """Returns total duration in minutes"""
        from datetime import timedelta
        total = sum(
            (video.duration.total_seconds() for video in self.videos.all() if video.duration),
            timedelta()
        )
        return round(total.total_seconds() / 60, 1)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True},
        related_name='taught_courses'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/',
        blank=True,
        null=True
    )
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Courses'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Course.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    def get_total_duration(self):
        """Calculate total course duration in minutes"""
        from datetime import timedelta
        total = sum(
            (video.duration.total_seconds() for video in self.videos.all() if video.duration),
            timedelta()
        )
        return total.total_seconds() / 60

    def get_student_count(self):
        """Count unique students enrolled in the course"""
        return (self.enrollments
                .filter(user__is_teacher=False)
                .distinct('user')
                .count())

    def increment_view_count(self):
        """Atomically increment view count"""
        self.view_count = models.F('view_count') + 1
        self.save(update_fields=['view_count'])