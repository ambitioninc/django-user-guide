from django.auth.models import User
from django.test import TestCase
from django_dynamic_fixture import G
from mock import Mock

from user_guide import models, views


class GuideSeenTest(TestCase):

    def test_post(self):
        user = G(User)
        guide_info = G(models.GuideInfo, user=user)
        request = Mock(POST={
            'id': guide_info.id,
            'is_finished': True
        })

        self.assertEqual(views.post(request).status_code, 200)
        self.assertEqual(
            models.GuideInfo.objects.get(id=guide_info.id),
            is_finished=True
        )
