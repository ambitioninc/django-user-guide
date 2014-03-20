from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from tastypie.api import NamespacedApi

from user_guide.api import GuideResource, GuideInfoResource


user_guide_api = NamespacedApi(api_name='api', urlconf_namespace='user_guide')
user_guide_api.register(GuideResource())
user_guide_api.register(GuideInfoResource())

urlpatterns = patterns(
    '',
    url(r'', include(user_guide_api.urls, namespace='user_guide'))
)
