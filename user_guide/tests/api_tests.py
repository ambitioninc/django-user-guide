from django.contrib.auth.models import User
from django_dynamic_fixture import G
from freezegun import freeze_time
from tastypie.test import ResourceTestCase

from user_guide.models import Guide, GuideInfo


@freeze_time('2014-03-17')
class GuideInfoResourceTest(ResourceTestCase):
    def setUp(self):
        super(GuideInfoResourceTest, self).setUp()

        self.users = [
            User.objects.create_user(
                password='test',
                username='test{0}@test.com'.format(i),
                email='test{0}@test.com'.format(i)
            )
            for i in xrange(0, 2)
        ]

        self.guides = [
            G(Guide, html='<div>Hello test {0}!</div>'.format(i), guide_name='Test Guide {0}'.format(i))
            for i in xrange(0, 5)
        ]

    def test_get_guide_info_resource(self):

        # Make some guide info objects
        guide_infos = [G(GuideInfo, user=self.users[i], guide=self.guides[i]) for i in xrange(2)]

        # Should not allow unauthorize access
        resp = self.api_client.get('/api/guideinfo/', format='json')
        self.assertHttpUnauthorized(resp)

        # Log in and make a request
        self.api_client.client.login(username=self.users[0].username, password='test')
        resp = self.api_client.get('/api/guideinfo/', format='json', data={
            'guide__guide_name__in': ['Test Guide 0', 'Test Guide 1']
        })
        self.assertValidJSONResponse(resp)

        # Deserialize the response
        objects = self.deserialize(resp)['objects']

        # The response should look ok
        self.assertEqual(len(objects), 2)
        self.assertFalse(objects[0]['is_finished'])
        self.assertFalse(objects[1]['is_finished'])
        self.assertEqual(objects[0]['user']['email'], self.users[0].email)
        self.assertEqual(objects[1]['user']['email'], self.users[1].email)
        self.assertEqual(objects[0]['guide']['html'], guide_infos[0].guide.html)
        self.assertEqual(objects[1]['guide']['html'], guide_infos[1].guide.html)
        self.assertEqual(objects[0]['guide']['creation_time'], '2014-03-17T00:00:00')
        self.assertEqual(objects[1]['guide']['creation_time'], '2014-03-17T00:00:00')

    def test_put_guide_info_resource(self):
        guide_infos = [
            G(GuideInfo, user=self.users[0], guide=self.guides[0]),
            G(GuideInfo, user=self.users[0], guide=self.guides[1]),
            G(GuideInfo, user=self.users[1], guide=self.guides[1])
        ]

        # Try to put when logged out
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[2].id), format='json')
        self.assertHttpUnauthorized(resp)

        # Log in as users[0]
        self.api_client.client.login(username=self.users[0].username, password='test')

        # Try to put on another account's guide info object
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[2].id), format='json', data={
            'is_finished': True
        })
        self.assertHttpUnauthorized(resp)

        # Try to put no data
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[0].id), format='json')
        self.assertHttpBadRequest(resp)

        # Try to put bad data
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[0].id), format='json', data={
            'guide': 1
        })
        self.assertEqual(resp.content, 'Can only update fields: is_finished')
        self.assertHttpBadRequest(resp)

        # Should be able to update the finished field
        resp = self.api_client.put('/api/guideinfo/{0}/'.format(guide_infos[0].id), format='json', data={
            'is_finished': True
        })
        self.assertHttpAccepted(resp)

        # The guide should have been updated by the put request
        updated_guide_info = GuideInfo.objects.get(id=guide_infos[0].id)
        self.assertTrue(updated_guide_info.is_finished)
        self.assertIsNotNone(updated_guide_info.finished_time)
