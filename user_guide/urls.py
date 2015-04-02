from django.conf.urls import patterns, url

from user_guide import views


urlpatterns = patterns(
    '',
    url(r'/seen/', views.GuideSeenView.as_view(), name='user_guide.seen')
)
