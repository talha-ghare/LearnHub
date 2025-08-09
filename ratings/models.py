from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class CourseRating(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} rated {self.course.title} {self.rating} stars"