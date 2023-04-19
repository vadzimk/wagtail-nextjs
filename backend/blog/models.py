from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag, TaggedItemBase

from blog.blocks import BodyBlock


class BlogPage(Page):
    description = models.CharField(max_length=255, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full")
    ]


class PostPage(Page):
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    body = StreamField(BodyBlock(), blank=True)
    tags = ClusterTaggableManager(through='blog.PostPageTag', blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        InlinePanel('categories', label='category'),
        FieldPanel('tags'),
        StreamFieldPanel('body')
    ]


content_panels = Page.content_panels + [
    ImageChooserPanel("header_image"),
    InlinePanel('categories', label='category'),
    FieldPanel('tags'),
    StreamFieldPanel('body'),
]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class PostPageBlogCategory(models.Model):
    page = ParentalKey("blog.PostPage",
                       on_delete=models.CASCADE,
                       related_name='categories'
                       )
    blog_category = models.ForeignKey('blog.BlogCategory',
                                      on_delete=models.CASCADE,
                                      related_name='post_pages'
                                      )
    panels = [
        SnippetChooserPanel('blog_category')
    ]

    class Meta:
        unique_together = ['page', 'blog_category']


class PostPageTag(TaggedItemBase):
    content_object = ParentalKey("PostPage",
                                 related_name='post_tags')
