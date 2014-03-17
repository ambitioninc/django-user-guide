from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from freezegun import freeze_time
from user_guide.models import Guide


@freeze_time('2014-03-17 00:00:00')
class GuideTest(TestCase):
    def test_guide_creation(self):
        user = User.objects.create(username='test@test.com', email='test@test.com', password='test123')
        guide = Guide.objects.create(
            html='<div>Hello Test!</div>',
            view_class_name = 'TestView',
            guide_type='Window'
        )

        self.assertEqual(guide.creation_time, datetime(2014, 03, 17, 0, 0, 0))
