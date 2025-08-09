from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models  # Added this import
from .models import Course, Topic
from .forms import CourseForm, TopicForm
from django.db.models import Q

def course_list(request):
    try:
        courses = Course.objects.all().select_related('teacher', 'topic')
        topics = Topic.objects.all()
        
        # Search functionality - Parentheses now properly closed
        search_query = request.GET.get('search', '')
        if search_query:
            courses = courses.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(teacher__username__icontains=search_query) |
                Q(topic__name__icontains=search_query)
            )  # This parenthesis was missing
        
        # Topic filtering
        topic_filter = request.GET.get('topic')
        if topic_filter:
            courses = courses.filter(topic__slug=topic_filter)
        
        context = {
            'courses': courses,
            'topics': topics,
            'selected_topic': topic_filter,
            'search_query': search_query
        }
        return render(request, 'courses/course_list.html', context)
    
    except Exception as e:
        messages.error(request, 'Error loading courses. Please try again.')
        return render(request, 'courses/course_list.html', {'courses': [], 'topics': []})

def topic_list(request):
    try:
        topics = Topic.objects.all()
        return render(request, 'courses/topic_list.html', {'topics': topics})
    except Exception as e:
        messages.error(request, 'Error loading topics.')
        return render(request, 'courses/topic_list.html', {'topics': []})

def topic_detail(request, slug):
    try:
        topic = get_object_or_404(Topic, slug=slug)
        courses = Course.objects.filter(topic=topic).select_related('teacher')
        return render(request, 'courses/topic_detail.html', {
            'topic': topic,
            'courses': courses
        })
    except Http404:
        raise
    except Exception as e:
        messages.error(request, 'Error loading topic details.')
        return redirect('topic_list')

def course_detail(request, slug):
    try:
        course = get_object_or_404(Course, slug=slug)
        videos = course.videos.all()
        
        # Check if user is authenticated before counting view
        if request.user.is_authenticated:
            course.increment_views()
        
        # Calculate average rating safely
        rating_agg = course.ratings.aggregate(models.Avg('rating'))
        avg_rating = rating_agg['rating__avg'] if rating_agg else None
        
        context = {
            'course': course,
            'videos': videos,
            'is_teacher': request.user.is_authenticated and request.user == course.teacher,
            'average_rating': avg_rating
        }
        return render(request, 'courses/course_detail.html', context)
    
    except Http404:
        raise
    except Exception as e:
        messages.error(request, 'Error loading course details.')
        return redirect('course_list')

@login_required
def create_course(request):
    if not getattr(request.user, 'is_teacher', False):
        messages.error(request, 'Only teachers can create courses.')
        return redirect('course_list')
    
    try:
        if request.method == 'POST':
            form = CourseForm(request.POST, request.FILES)
            if form.is_valid():
                course = form.save(commit=False)
                course.teacher = request.user
                course.save()
                messages.success(request, 'Course created successfully!')
                return redirect('course_detail', slug=course.slug)
        else:
            form = CourseForm()
        
        return render(request, 'courses/create_course.html', {'form': form})
    
    except Exception as e:
        messages.error(request, 'Error creating course. Please try again.')
        return redirect('course_list')

@login_required
def create_topic(request):
    if not getattr(request.user, 'is_teacher', False):
        messages.error(request, 'Only teachers can create topics.')
        return redirect('topic_list')
    
    try:
        if request.method == 'POST':
            form = TopicForm(request.POST)
            if form.is_valid():
                topic = form.save()
                messages.success(request, f'Topic "{topic.name}" created successfully!')
                return redirect('topic_detail', slug=topic.slug)
        else:
            form = TopicForm()
        
        return render(request, 'courses/create_topic.html', {'form': form})
    
    except Exception as e:
        messages.error(request, 'Error creating topic. Please try again.')
        return redirect('topic_list')