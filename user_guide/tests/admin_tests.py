from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django_dynamic_fixture import G, F

from user_guide.admin import GuideAdmin, GuideInfoAdmin
from user_guide.models import Guide, GuideInfo


class AdminTest(TestCase):
    def setUp(self):
        super(AdminTest, self).setUp()
        self.site = AdminSite()

    def test_user_guide_admin(self):
        guide_admin = GuideAdmin(Guide, self.site)
        self.assertEqual(guide_admin.list_display, ('guide_name', 'guide_tag', 'guide_importance', 'creation_time'))

    def test_user_guide_info_admin(self):
        guide_info_admin = GuideInfoAdmin(GuideInfo, self.site)
        guide_info_obj = G(GuideInfo, guide=F(guide_name='test_name'))
        self.assertEqual(guide_info_admin.list_display, ('user', 'guide_name', 'is_finished', 'finished_time'))
        self.assertEqual(guide_info_admin.guide_name(guide_info_obj), 'test_name')
