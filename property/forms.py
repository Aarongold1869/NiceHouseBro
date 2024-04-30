from django import forms
from .models import Comment, Reply

class CommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Leave a comment...'}))
    
    class Meta:
        model = Comment
        fields = ['text']

class ReplyForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Post a reply...'}))
    
    class Meta:
        model = Reply
        fields = ['text']