from django import forms
from .models import Comment, Reply, ReportForm

class CommentForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Leave a comment...', 'rows': 2}))
    
    class Meta:
        model = Comment
        fields = ['text']

class ReplyForm(forms.ModelForm):
    text = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Post a reply...', 'rows': 2}))
    
    class Meta:
        model = Reply
        fields = ['text']

class ReportFormForm(forms.ModelForm):
    
    class Meta:
        model = ReportForm
        fields = ['cause']