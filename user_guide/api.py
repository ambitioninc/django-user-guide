from user_guide.modles import Guide
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import NamespacedModelResource, ALL


class GuideResource(NamespacedModelResource):
    class Meta:
        urlconf_namespace = 'account'
        queryset = Guide.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        filtering = {
            'id': ['exact'],
            'name': ['exact'],
            'creation_time': ALL
        }
