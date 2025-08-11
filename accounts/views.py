# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from courses.models import Course
from videos.models import Bookmark


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    context = {}
    
    if request.user.is_teacher():
        # Teacher dashboard
        my_courses = Course.objects.filter(teacher=request.user)
        context.update({
            'courses': my_courses,  # Changed from 'my_courses' to 'courses' to match template
            'total_courses': my_courses.count(),
            'total_videos': sum(course.videos.count() for course in my_courses)
        })
        template = 'accounts/teacher_dashboard.html'
    else:
        # Student dashboard
        bookmarked_videos = Bookmark.objects.filter(user=request.user).select_related('video', 'video__course')
        recent_courses = Course.objects.all()[:6]
        context.update({
            'bookmarked_videos': bookmarked_videos,
            'recent_courses': recent_courses,
            'total_bookmarks': bookmarked_videos.count()
        })
        template = 'accounts/student_dashboard.html'
    
    return render(request, template, context)


@login_required
def profile_view(request):
    """
    Profile view that redirects to appropriate dashboard.
    Since LearnHub uses role-based dashboards instead of traditional profile pages,
    we redirect users to their personalized dashboard.
    """
    return redirect('dashboard')
