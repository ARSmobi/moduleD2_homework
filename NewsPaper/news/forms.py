from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author',
                  'categoryType']
        labels = {
            'title': 'Название',
            'text': 'Текст',
            'author': 'Автор',
            'categoryType': 'Тип поста',
        }
