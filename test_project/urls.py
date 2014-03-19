from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import TestProjectView

# Enable admin section
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^user-guide/', include('user_guide.urls', 'user_guide')),
    url(r'^test-view/$', TestProjectView.as_view(), name='test_project.test_view'),
    url(r'^admin/', include(admin.site.urls))
)
