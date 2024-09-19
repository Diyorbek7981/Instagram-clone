from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('author', 'category')
    list_display_links = ('author', 'category')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
    list_display_links = ('author', 'post')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
    list_display_links = ('author', 'post')


@admin.register(PostSave)
class PostSaveAdmin(admin.ModelAdmin):
    list_display = ('author', 'post')
    list_display_links = ('author', 'post')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment')
    list_display_links = ('author', 'comment')
