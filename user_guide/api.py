from datetime import datetime

from django.contrib.auth.models import User
from tastypie import fields, http
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import NamespacedModelResource, ALL, ALL_WITH_RELATIONS

from user_guide.models import Guide, GuideInfo


class GuideUserResource(NamespacedModelResource):
    """
    Tastypie resource for guide users. Not exposed via url, does not allow any REST methods.
    Only used by the GuideInfoResource.
    """
    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = User.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        list_allowed_methods = []
        fields = ['email', 'date_joined']
        filtering = {
            'id': ['exact'],
            'email': ['exact']
        }
        ordering = {
            'id': ALL,
            'email': ALL
        }


class GuideResource(NamespacedModelResource):
    """
    Tastypie resource for guides. Accessible via url, only allows GET method.
    """
    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = Guide.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        list_allowed_methods = ['get']
        filtering = {
            'id': ['exact'],
            'guide_name': ALL_WITH_RELATIONS,
            'guide_tag': ALL_WITH_RELATIONS,
            'creation_time': ALL_WITH_RELATIONS
        }
        ordering = {
            'id': ['exact'],
            'name': ['exact'],
            'creation_time': ALL_WITH_RELATIONS
        }


class GuideInfoResource(NamespacedModelResource):
    """
    Tastypie resource for guide info. Accessible via url, allows GET and PUT methods.
    """
    user = fields.ForeignKey(GuideUserResource, 'user', full=True)
    guide = fields.ForeignKey(GuideResource, 'guide', full=True)

    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = GuideInfo.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        list_allowed_methods = ['get', 'put']
        fields_allowed_update = ['is_finished']
        filtering = {
            'id': ['exact'],
            'is_finished': ALL,
            'finished_time': ALL_WITH_RELATIONS,
            'guide': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS
        }
        ordering = {
            'id': ['exact'],
            'is_finished': ALL,
            'finished_time': ALL_WITH_RELATIONS,
            'guide': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS
        }

    def alter_deserialized_detail_data(self, request, deserialized):
        """
        Enforces that the request conforms to PUT guidelines.
            - A user can only update the fields specified in fields_allowed_update.
        """
        if set(deserialized.keys()) - set(self._meta.fields_allowed_update):
            raise ImmediateHttpResponse(
                response=http.HttpBadRequest('Can only update fields: {0}'.format(
                    ', '.join(self._meta.fields_allowed_update)
                ))
            )

        # Update the finished time
        deserialized['finished_time'] = datetime.utcnow()

        return super(GuideInfoResource, self).alter_deserialized_detail_data(request, deserialized)

    def put_detail(self, request, **kwargs):
        """
        Enforces that the request conforms to PUT guidelines.
            - A user can only update the fields specified in fields_allowed_update.
        """
        guide_info = GuideInfo.objects.get(pk=kwargs.get('pk'))

        if guide_info.user.id != request.user.id:
            raise ImmediateHttpResponse(
                response=http.HttpUnauthorized('PUT user must match request\'s user.')
            )

        return super(GuideInfoResource, self).put_detail(request, **kwargs)
