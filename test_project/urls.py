from django.conf.urls import patterns, include, url
from django.contrib import admin

# Enable admin section
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^user-guide/', include('user_guide.urls', 'user_guide')),
    url(r'^admin/', include(admin.site.urls))
)
