from django.shortcuts import render
from django.urls import path
from rest_framework import serializers
from wagtail.api.v2.views import BaseAPIViewSet, PagesAPIViewSet
from wagtail.models import Page

from blog.models import BlogCategory
from blog.serializers import CategorySerializer, TagSerializer


class CategoryAPIViewSet(BaseAPIViewSet):
    base_serializer_class = CategorySerializer
    # https://www.django-rest-framework.org/api-guide/filtering/#filter-backends
    # https://docs.wagtail.io/en/stable/advanced_topics/api/v2/views.html#filter-backends
    filter_backends = []
    meta_fields = []
    body_fields = ['id', 'slug', 'name']  # fields to include in the request body and response body.
    listing_default_fields = ['id', 'slug', 'name']  # fields to include in the response when the viewset is used for listing objects
    nested_default_fields = []  # fields to include when the viewset is used for nested serialization
    name = 'category'  # refers in url routing
    model = BlogCategory


class TagAPIViewSet(BaseAPIViewSet):
    base_serializer_class = TagSerializer
    filter_backends = []
    meta_fields = []
    body_fields = ['id', 'slug', 'name']
    nested_default_fields = []
    name='tag'
    model ='tag'

class PageRelativeUrlListAPIViewSet(PagesAPIViewSet):
    """ return all pages and their relative url """
    model = Page

    def get_serializer(self, qs, many=True):
        return PageRelativeUrlListAPIViewSet(qs, many=many)

    @classmethod
    def get_urlpatterns(cls):
        return [path('', cls.as_view({'get': 'listing_view'}), name='listing')]
