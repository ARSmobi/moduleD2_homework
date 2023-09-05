from django_filters import FilterSet, filters
from .models import Post


class PostFilter(FilterSet):
    dateCreation = filters.DateFilter(label='Дата', lookup_expr='gt')
    title = filters.CharFilter(label='Название', lookup_expr='iregex')
    author = filters.CharFilter(label='Автор', lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['author', 'title', 'dateCreation']
