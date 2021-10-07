from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django import forms
from .models import Group, Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = {'group', 'text', 'image'}


class CommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = {'text', 'img'}