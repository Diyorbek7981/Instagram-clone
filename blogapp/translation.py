from .models import *
from modeltranslation.translator import TranslationOptions, register


@register(Posts)
class PostsTranslationOptions(TranslationOptions):
    fields = ('caption',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
