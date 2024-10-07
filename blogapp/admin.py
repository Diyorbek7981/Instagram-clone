from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


# Register your models here.
class TaskAdmin():
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Category)
class CategoryAdmin(TranslationAdmin, TaskAdmin):
    list_display = ('name',)
    list_display_links = ('name',)


@admin.register(Posts)
class PostsAdmin(TranslationAdmin, TaskAdmin):
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
