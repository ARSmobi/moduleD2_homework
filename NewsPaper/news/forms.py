from django.forms import ModelForm
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author',
                  'categoryType',
                  'postCategory']
        labels = {
            'title': 'Название',
            'text': 'Текст',
            'author': 'автор',
            'categoryType': 'Тип поста',
            'postCategory': 'Категория'
        }
        widgets = {
            'postCategory': forms.CheckboxSelectMultiple(attrs={
                'value': model.author
            })
        }


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get_or_create(name='common')[0]
        common_group.user_set.add(user)
        return user
