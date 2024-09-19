from django.shortcuts import render
from rest_framework import generics, permissions
from .models import *
from .serializers import *


# Create your views here.

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Posts.objects.all()
