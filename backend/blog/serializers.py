from rest_framework import serializers
from rest_framework.fields import Field
from wagtail import fields
from wagtail.api.v2.serializers import StreamField
from wagtail.api.v2 import serializers as wagtail_serializers
from blog.models import PostPage, BlogCategory, Tag, BlogPage, BasePage
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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'slug', 'name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'slug', 'name']


class BasePageSerializer(serializers.ModelSerializer):
    serializer_field_mapping = serializers.ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping.update({
        fields.StreamField: wagtail_serializers.StreamField
    })
    class Meta:
        model = BasePage
        fields = ['id',
                  'slug',
                  'title',
                  'url',
                  'last_published_at']

class BlogPageSerializer(BasePageSerializer):
    class Meta:
        model = BlogPage
        fields = BasePageSerializer.Meta.fields


class PostPageSerializer(serializers.ModelSerializer):
    tags = TagField()
    categories = CategoryField()
    body = StreamField()
    header_image = ImageRenditionField('max-1000x800')

    class Meta:
        model = PostPage
        fields = BasePageSerializer.Meta.fields + [
                  'tags',
                  'categories',
                  'body',
                  'header_image']


class PageRelativeUrlListSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return {
            'title': instance.title,
            'relative_url': instance.url,
        }

