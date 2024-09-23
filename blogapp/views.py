from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .paginations import CustomPageNumberPagination
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


# Create your views here.

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Posts.objects.all()


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Post updated successfully",
                "data": serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                "success": True,
                "code": status.HTTP_200_OK,
                "message": "Post deleted successfully",
            }
        )

# create
