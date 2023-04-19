from rest_framework import serializers
from rest_framework.fields import Field
from wagtail.api.v2.serializers import StreamField

from blog.models import PostPage, BlogCategory, Tag
from wagtail.images.api.fields import ImageRenditionField

class TagField(Field):
    def to_representation(self, tags):
        try:
            return [
                {'name': tag.name,
                 'slug': tag.slug,
                 'id': tag.id}
                for tag in tags.all()
            ]
        except Exception:
            return []

class CategoryField(Field):
    def to_representation(self, categories):
        try:
            return [
                {'name': category.blog_category.name,
                 'slug': category.blog_category.slug,
                 'id': category.blog_category.id}
                for category in categories.all()
            ]
        except:
            return []

class PostPageSerializer(serializers.ModelSerializer):
    tags = TagField()
    categories = CategoryField()
    body = StreamField()
    header_image = ImageRenditionField('max-1000x800')


    class Meta:
        model = PostPage
        fields = ['id', 'slug', 'title', 'tags', 'categories', 'body']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'slug', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'slug', 'name']
