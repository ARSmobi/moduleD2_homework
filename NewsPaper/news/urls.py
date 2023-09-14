from django.urls import path
from .views import PostDetail, AddPost, PostList, PostUpdate, PostDelete
from .views import upgrade_to_author

app_name = 'news'

urlpatterns = [
    path('search/', PostList.as_view(), name='posts'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add/', AddPost.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_to_author, name='upgrade'),
]
