## videos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Video, Bookmark, Comment
from .forms import VideoForm, CommentForm
from courses.models import Course

@login_required
def upload_video(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Only course teacher can upload videos
    if request.user != course.teacher:
        messages.error(request, 'You can only upload videos to your own courses.')
        return redirect('course_detail', slug=course.slug)
    
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course
            video.save()
            messages.success(request, 'Video uploaded successfully!')
            return redirect('course_detail', slug=course.slug)
    else:
        form = VideoForm()
    
    return render(request, 'videos/upload_video.html', {
        'form': form,
        'course': course
    })

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    comments = video.comments.all().select_related('user')
    
    # Check if user has bookmarked this video
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, video=video).exists()
    
    # Handle comment form
    comment_form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.video = video
                comment.save()
                messages.success(request, 'Comment added successfully!')
                return redirect('video_detail', video_id=video.id)
        else:
            comment_form = CommentForm()
    
    context = {
        'video': video,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
        'comment_form': comment_form,
    }
    return render(request, 'videos/video_detail.html', context)

@login_required
@require_POST
def toggle_bookmark(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user, 
        video=video
    )
    
    if not created:
        bookmark.delete()
        bookmarked = False
        message = 'Bookmark removed'
    else:
        bookmarked = True
        message = 'Video bookmarked'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'bookmarked': bookmarked,
            'message': message
        })
    
    messages.success(request, message)
    return redirect('video_detail', video_id=video.id)

@login_required
def add_comment(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = video
            comment.save()
            messages.success(request, 'Comment added successfully!')
    
    return redirect('video_detail', video_id=video.id)
