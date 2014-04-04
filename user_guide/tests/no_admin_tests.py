from django.conf import settings
from django.test import TestCase

from user_guide import admin


class NoAdminTest(TestCase):
    """
    Tests loading of the admin module when django.contrib.admin is not installed.
    """
    def test_no_admin(self):
        with self.settings(INSTALLED_APPS=[app for app in settings.INSTALLED_APPS if app != 'django.contrib.admin']):
            reload(admin)
            self.assertIsNotNone(admin)
