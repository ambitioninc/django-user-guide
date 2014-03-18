from datetime import datetime

from django.contrib.auth.models import User
from freezegun import freeze_time
from tastypie.test import ResourceTestCase
from user_guide.models import Guide, GuideInfo


@freeze_time('2014-03-17 00:00:00')
class GuideInfoResourceTest(ResourceTestCase):
    def setUp(self):
        super(GuideInfoResourceTest, self).setUp()

        self.users = [
            User.objects.create_user(
                username='test{0}@test.com'.format(i),
                email='test{0}@test.com'.format(i),
                password='test'
            )
            for i in xrange(0, 5)
        ]

        self.guides = [
            Guide.objects.create(
                html='<div>Hello test {0}!</div>'.format(i),
                view_class_name='TestView',
                guide_name='Test Guide {0}'.format(i),
                guide_type='Window'
            )
            for i in xrange(0, 5)
        ]

    def test_get_guide_info_resource(self):
        # Create a few guide info objects
        GuideInfo.objects.create(
            user=self.users[0],
            guide=self.guides[0]
        )
        GuideInfo.objects.create(
            user=self.users[1],
            guide=self.guides[1]
        )

        # Should not allow unauthorize access
        resp = self.api_client.get('/api/guideinfo/', format='json')
        self.assertHttpUnauthorized(resp)

        # Log in and make a request
        self.api_client.client.login(username='test0@test.com', password='test')
        resp = self.api_client.get('/api/guideinfo/', format='json', data={
            'guide__view_class_name': 'TestView',
            'order_by': 'user__email'
        })
        self.assertValidJSONResponse(resp)

        # Deserialize the response
        objects = self.deserialize(resp)['objects']

        # The response should look ok
        self.assertEqual(len(objects), 2)
        self.assertFalse(objects[0]['finished'])
        self.assertFalse(objects[1]['finished'])
        self.assertEqual(objects[0]['user']['email'], self.users[0].email)
        self.assertEqual(objects[1]['user']['email'], self.users[1].email)
        self.assertEqual(objects[0]['guide']['html'], '<div>Hello test 0!</div>')
        self.assertEqual(objects[1]['guide']['html'], '<div>Hello test 1!</div>')
        self.assertEqual(objects[0]['guide']['creation_time'], '2014-03-17T00:00:00')
        self.assertEqual(objects[1]['guide']['creation_time'], '2014-03-17T00:00:00')

    def test_post_guide_info_resource(self):
        guide_infos = [
            GuideInfo.objects.create(
                user=self.users[0],
                guide=self.guides[0]
            ),
            GuideInfo.objects.create(
                user=self.users[0],
                guide=self.guides[1]
            ),
            GuideInfo.objects.create(
                user=self.users[1],
                guide=self.guides[1]
            )
        ]

        # Try to put when logged out
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[2].id), format='json')
        self.assertHttpUnauthorized(resp)

        # Log in as users[0]
        self.api_client.client.login(username='test0@test.com', password='test')

        # Try to put on another account's guide info object
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[2].id), format='json', data={
            'finished': True
        })
        self.assertHttpBadRequest(resp)

        # Try to put no data
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[0].id), format='json')
        self.assertHttpBadRequest(resp)

        # Try to put bad data
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[0].id), format='json', data={
            'guide': 1
        })
        self.assertEqual(resp.content, 'Can only update fields: finished')
        self.assertHttpBadRequest(resp)

        # Should be able to update the finished field
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[0].id), format='json', data={
            'finished': True
        })
        self.assertHttpAccepted(resp)

        # The guide should have been updated by the put request
        updated_guide_info = GuideInfo.objects.get(id=guide_infos[0].id)
        self.assertTrue(updated_guide_info.finished)
        self.assertEqual(updated_guide_info.finished_time, datetime.now())
