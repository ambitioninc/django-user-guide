from django.contrib.auth.models import User
from freezegun import freeze_time
from tastypie.test import ResourceTestCase
from user_guide.models import Guide, GuideInfo


@freeze_time('2014-03-17 00:00:00')
class GuideInfoResourceTest(ResourceTestCase):
    def test_guide_info_resource(self):
        users = [
            User.objects.create_user(username='test@test.com', email='test@test.com', password='test'),
            User.objects.create_user(username='test2@test.com', email='test2@test.com', password='test')
        ]
        guide = Guide.objects.create(
            html='<div>Hello Test</div>',
            view_class_name='TestView',
            guide_name='Test Guide',
            guide_type='Window'
        )

        # Create a few guide info objects
        GuideInfo.objects.create(
            user=users[0],
            guide=guide
        )
        GuideInfo.objects.create(
            user=users[1],
            guide=guide
        )

        self.api_client.client.login(username='test@test.com', password='test')
        resp = self.api_client.get('/api/guideinfo/', format='json', data={
            'guide__view_class_name': 'TestView',
            'order_by': '-user__email'
        })

        self.assertValidJSONResponse(resp)
        objects = self.deserialize(resp)['objects']
        self.assertEqual(len(objects), 2)
        self.assertEqual(objects[0]['user']['email'], users[0].email)
        self.assertEqual(objects[0]['guide']['html'], '<div>Hello Test</div>')
        self.assertEqual(objects[0]['guide']['creation_time'], '2014-03-17T00:00:00')
        #self.assertEqual(len(guides), 1)
