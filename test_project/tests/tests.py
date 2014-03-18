from django.test import TestCase


class SampleTest(TestCase):
    def test_1_equals_1(self):
        self.assertEquals(1, 1)

    def test_2_equals_2(self):
        self.assertEquals(2, 2)

    def test_3_equals_3(self):
        self.assertEquals(3, 3)
