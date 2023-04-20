from django.urls import path, include
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.core import urls as wagtail_urls

from blog.views import CategoryAPIViewSet, TagAPIViewSet, PageRelativeUrlListAPIViewSet

api_router = WagtailAPIRouter('api')  # url namespace
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('category', CategoryAPIViewSet)
api_router.register_endpoint('tag', TagAPIViewSet)
api_router.register_endpoint('page_relative_urls', PageRelativeUrlListAPIViewSet)

app_name = 'blog'

urlpatterns = [
    path('v1/', api_router.urls),
]
