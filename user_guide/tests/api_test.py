#import json

from django.contrib.auth.models import User
from freezegun import freeze_time
from tastypie.test import ResourceTestCase
from user_guide.models import Guide, GuideInfo


@freeze_time('2014-03-17 00:00:00')
class GuideInfoResourceTest(ResourceTestCase):
    def test_guide_info_resource(self):
        user = User.objects.create(username='test@test.com', email='test@test.com', password='test')
        guide = Guide.objects.create(
            html='<div>Hello Test!</div>',
            view_class_name='TestView',
            guide_name='Test Guide',
            guide_type='Window'
        )
        GuideInfo.objects.create(
            user=user,
            guide=guide
        )

        self.api_client.client.login(username='test@test.com', password='test', format='json', data={
            'guide__view_class_name': 'TestView',
            'user': user.id
        })
        resp = self.api_client.get('/user-guide/guideinfo')
        print resp
        self.assertEqual(1, 0)
        #self.assertEqual(len(guides), 1)
