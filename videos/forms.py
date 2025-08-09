### videos/forms.py

from django import forms
from .models import Video, Comment

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-textarea'})
