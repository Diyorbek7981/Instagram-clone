from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('retrive_update/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-destroy'),
]
