from django.contrib.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G
from mock import Mock

from user_guide import models, views


class GuideSeenTest(TestCase):

    def test_post(self):
        user = G(User)
        guide_info = G(models.GuideInfo, user=user)
        request = Mock(user=user, POST={
            'id': guide_info.id,
            'is_finished': True
        })
        view = views.GuideSeenView()

        self.assertEqual(view.post(request).status_code, 200)
        self.assertTrue(models.GuideInfo.objects.get(id=guide_info.id).is_finished)

    def test_post_wrong_user(self):
        user1 = G(User)
        user2 = G(User)
        guide_info = G(models.GuideInfo, user=user1)
        request = Mock(user=user2, POST={
            'id': guide_info.id,
            'is_finished': True
        })
        view = views.GuideSeenView()

        self.assertEqual(view.post(request).status_code, 200)
        self.assertFalse(models.GuideInfo.objects.get(id=guide_info.id).is_finished)
