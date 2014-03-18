from datetime import datetime

from django.contrib.auth.models import User
from tastypie import fields, http
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import NamespacedModelResource, ALL, ALL_WITH_RELATIONS
from user_guide.models import Guide, GuideInfo


class GuideUserResource(NamespacedModelResource):

    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = User.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        list_allowed_methods = ['get']
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

    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = Guide.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        filtering = {
            'id': ['exact'],
            'view_class_name': ALL,
            'creation_time': ALL_WITH_RELATIONS
        }
        ordering = {
            'id': ['exact'],
            'name': ['exact'],
            'creation_time': ALL_WITH_RELATIONS
        }


class GuideInfoResource(NamespacedModelResource):
    user = fields.ForeignKey(GuideUserResource, 'user', full=True)
    guide = fields.ForeignKey(GuideResource, 'guide', full=True)

    class Meta:
        urlconf_namespace = 'user_guide'
        queryset = GuideInfo.objects.all()
        authorization = Authorization()
        authentication = SessionAuthentication()
        list_allowed_methods = ['get', 'put']
        fields_allowed_update = ['finished']
        filtering = {
            'id': ['exact'],
            'finished': ALL,
            'finished_time': ALL_WITH_RELATIONS,
            'guide': ALL_WITH_RELATIONS,
            'user': ALL_WITH_RELATIONS
        }
        ordering = {
            'id': ['exact'],
            'finished': ALL,
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

        deserialized['finished_time'] = datetime.now()

        return super(GuideInfoResource, self).alter_deserialized_detail_data(request, deserialized)

    def put_detail(self, request, **kwargs):
        """
        Enforces that the request conforms to PUT guidelines.
            - A user can only update the fields specified in fields_allowed_update.
        """
        guide_info = GuideInfo.objects.get(pk=kwargs.get('pk'))

        if guide_info.user.id != request.user.id:
            raise ImmediateHttpResponse(
                response=http.HttpBadRequest('User must match request\'s user.')
            )

        super(GuideInfoResource, self).put_detail(request, **kwargs)
