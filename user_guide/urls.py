from django.conf.urls import patterns, include, url
from tastypie.api import NamespacedApi
from user_guide.api import GuideResource

user_guide_api = NamespacedApi(api_name='api', urlconf_namespace='user_guide')

user_guide_api.register(GuideResource())

urlpatterns = patterns(
    '',
    url(r'', include(user_guide_api.urls, namespace='user_guide')),
)
