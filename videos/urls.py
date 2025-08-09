### videos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/<int:course_id>/', views.upload_video, name='upload_video'),
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('<int:video_id>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('<int:video_id>/comment/', views.add_comment, name='add_comment'),
]