### courses/admin.py

from django.contrib import admin
from .models import Course, Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'topic', 'created_at')
    list_filter = ('topic', 'created_at', 'teacher')
    search_fields = ('title', 'description', 'teacher__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('teacher',)