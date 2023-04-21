from django.db import models
from django.http import JsonResponse
from django.utils.module_loading import import_string
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from taggit.models import Tag as TaggitTag, TaggedItemBase

from blog.blocks import BodyBlock


class BasePage(Page):
    serializer_class = None

    class Meta:
        abstract = True

    def get_component_data(self):
        if not self.serializer_class:
            raise Exception(f'serializer_class is not set {self.__class__.__name__}')

        serializer_class = import_string(self.serializer_class)

        return {
            'page_type': self.__class__.__name__,
            'page_context': serializer_class(self).data
        }

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context['page_component'] = self.get_component_data()
        if 'blog_page' not in context:
            context['blog_page'] = BlogPage.objects.first()
        context['page_component']['categories_list'] = self.categories_list(context)
        context['page_component']['tags_list'] = self.tags_list(context)
        return context

    def serve(self, request, *args, **kwargs):
        """ overrides BasePage.serve() that returns TemplateResponse """
        context = self.get_context(request, *args, **kwargs)
        return JsonResponse(context['page_component'])

    def categories_list(self, context):
        categories = BlogCategory.objects.all()
        blog_page = context['blog_page']
        data = [{'name': category.name,
                 'slug': category.slug,
                 'url': blog_page.url + blog_page.reverse_subpage(
                     'post_by_category',
                     args=(category.slug,)
                 )}
                for category in categories]
        return data

    def tag_list(self,  context):
        tags = Tag.objects.all
        blog_page = context['blog_page']
        data = [{'name': tag.name,
                 'slug': tag.slug,
                 'url': blog_page.url + blog_page.reverse_subpage(
                     'post_by_tag',
                     args=(tag.slug,)
                 )}
                for tag in tags]


class BlogPage(RoutablePageMixin, BasePage):
    # serializer_class = 'blog.serializers.BlogPageSerializer'
    description = models.CharField(max_length=255, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('description', classname='full')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['page_component']['children_posts'] = [
            post.get_component_data()
            for post in self.posts
        ]
        return context

    def get_posts(self):
        return PostPage.objects.descendant_of(self).live()

    @route(r'^tag/(?P<tag>[-w]+/$)')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.posts = self.get_posts().filter(tags__slug=tag)
        return self.serve(request)

    @route(r'category/?P(<category>[-\w]+/$)')
    def post_by_category(self, request, category, *args, **kwargs):
        self.posts = self.get_posts().filter(categories__blog_category__slug=category)
        return self.serve(request)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return self.serve(request)


class PostPage(BasePage):
    serializer_class = 'blog.serializers.PostPageSerializer'


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
