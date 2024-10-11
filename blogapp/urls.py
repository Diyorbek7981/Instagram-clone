from django.urls import path
from .views import *

urlpatterns = [
    path('list/', PostListView.as_view(), name='post-list'),
    path('retrive_update/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
    path('coment_create/<int:pk>', PostCommentCreateAPIView.as_view(), name='post-comment-create'),
    path('coment_list/<int:pk>', PostCommentListAPIView.as_view()),
    path('post_like/<int:pk>', PostLikeAPIView.as_view(), name='post-like'),
]
