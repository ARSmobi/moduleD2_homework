from django.urls import path
from .views import PostList, PostDetail, Post, SearchList, AddPost


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', SearchList.as_view()),
    path('add/', AddPost.as_view()),
]
