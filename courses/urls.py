### courses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<slug:slug>/', views.topic_detail, name='topic_detail'),
    path('create/', views.create_course, name='create_course'),
    path('<slug:slug>/', views.course_detail, name='course_detail'),
    path('create-topic/', views.create_topic, name='create_topic'),
]