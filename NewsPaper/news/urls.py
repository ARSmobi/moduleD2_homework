from django.urls import path
from .views import PostList, PostDetail, Posts, SearchList


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', SearchList.as_view()),
]
