from django.forms import ModelForm
from .models import Post
from django import forms


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название поста'
            }),
        }
