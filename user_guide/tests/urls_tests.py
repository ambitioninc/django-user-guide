from django.test import TestCase

from user_guide import urls


class UrlsTest(TestCase):
    def test_that_urls_are_defined(self):
        """
        Should have several urls defined.
        """
        self.assertEqual(len(urls.urlpatterns), 1)
        self.assertEqual(urls.urlpatterns[0].name, 'user_guide.seen')
