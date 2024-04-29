from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Leave a comment...'}))
    
    class Meta:
        model = Comment
        fields = ['comment']