from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import NamespacedModelResource, ALL, ALL_WITH_RELATIONS
from user_guide.modles import Guide, GuideInfo


class GuideUserResource(NamespacedModelResource):
    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = User.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        fields = ['email', 'date_joined']
        filtering = {'id': ['exact']}


class GuideResource(NamespacedModelResource):
    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = Guide.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        filtering = {
            'id': ['exact'],
            'name': ['exact'],
            'creation_time': ALL_WITH_RELATIONS
        },
        ordering = {
            'id': ['exact'],
            'name': ['exact'],
            'creation_time': ALL_WITH_RELATIONS
        }


class GuideInfoResource(NamespacedModelResource):
    user = fields.ForeignKey(GuideUserResource, 'guide_user', full=True)
    guide = fields.ForeignKey(GuideResource, 'guide', full=True)

    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = GuideInfo.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        filtering = {
            'id': ['exact'],
            'name': ['exact'],
            'finished': ALL,
            'finished_time': ALL_WITH_RELATIONS,
            'guide': ALL_WITH_RELATIONS,
            'user': ALL
        },
        ordering = {
            'id': ['exact'],
            'name': ['exact'],
            'finished': ALL,
            'finished_time': ALL_WITH_RELATIONS
        }
