from django.test import TestCase
from django_dynamic_fixture import G

from user_guide.models import Guide


class GuideTest(TestCase):

    def test_guide_unicode(self):
        print "im an idiot"
        guide_obj = G(Guide, guide_name='test_name')
        self.assertEqual(unicode(guide_obj), 'test_name')
