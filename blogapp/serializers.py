from rest_framework import serializers
from .models import *
from userapp.models import Users


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Users
        fields = ('id', 'username', 'photo')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    # owner = serializers.ReadOnlyField(
    #     source='author.username')
    category = CategorySerializer(read_only=True)
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comments_count')
    like_me = serializers.SerializerMethodField('get_like')
    save_me = serializers.SerializerMethodField('get_save')

    class Meta:
        model = Posts
        fields = (
            'id',
            'author',
            'photo',
            'category',
            'caption',
            'post_likes_count',
            'post_comments_count',
            'like_me',
            'save_me'
        )

    def get_post_likes_count(self, obj):
        return obj.likes.count()

    def get_post_comments_count(self, obj):
        return obj.comments.count()

    def get_like(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                like = PostLike.objects.get(author=request.user, post=obj)
                return True
            except PostLike.DoesNotExist:
                return False

        return False

    def get_save(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            try:
                save = PostSave.objects.get(author=request.user, post=obj)
                return True
            except PostSave.DoesNotExist:
                return False

        return False
