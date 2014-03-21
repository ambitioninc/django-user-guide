from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template import Template, Context
from django.test import TestCase

from user_guide.models import Guide, GuideInfo


class TemplateTagTest(TestCase):
    def setUp(self):
        super(TemplateTagTest, self).setUp()

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
                guide_name='Test Guide {0}'.format(i),
                guide_type='Window',
                guide_tag='tag{0}'.format(i),
                guide_importance=i
            )
            for i in xrange(0, 10)
        ]

    def test_user_guide_tags_no_user(self):
        t = Template('{% load user_guide_tags %}{% user_guide %}')
        c = Context({})
        self.assertEqual('', t.render(c))

    def test_user_guide_tags_no_filters(self):
        t = Template('{% load user_guide_tags %}{% user_guide %}')
        r = HttpRequest()
        r.user = self.users[0]
        c = Context({
            'request': r
        })

        # Create an info for each guide
        guide_infos = [GuideInfo.objects.create(user=self.users[0], guide=guide) for guide in self.guides]

        # Render the template
        rendered = t.render(c)

        # Make sure the correct guides show up, guide_order should apply here
        self.assertTrue('Hello test 9!' in rendered)
        self.assertTrue('data-guide="{0}"'.format(guide_infos[9].id) in rendered)
        self.assertTrue('Hello test 8!' in rendered)
        self.assertTrue('data-guide="{0}"'.format(guide_infos[8].id) in rendered)
        self.assertTrue('Hello test 7!' in rendered)
        self.assertTrue('data-guide="{0}"'.format(guide_infos[7].id) in rendered)
        self.assertTrue('Hello test 6!' in rendered)
        self.assertTrue('data-guide="{0}"'.format(guide_infos[6].id) in rendered)
        self.assertTrue('Hello test 5!' in rendered)
        self.assertTrue('data-guide="{0}"'.format(guide_infos[5].id) in rendered)
        self.assertTrue('Hello test 4!' not in rendered)  # Should not have rendered 6 guides
        self.assertTrue('Hello test 3!' not in rendered)  # Should not have rendered 7 guides
        self.assertTrue('Hello test 2!' not in rendered)  # Should not have rendered 8 guides
        self.assertTrue('Hello test 1!' not in rendered)  # Should not have rendered 9 guides
        self.assertTrue('Hello test 0!' not in rendered)  # Should not have rendered 10 guides
        self.assertTrue('django-user-guide.css' in rendered)  # Should have django-user-guide style sheet
        self.assertTrue('django-user-guide.js' in rendered)  # Should have django-user-guide script
        self.assertTrue('custom-style.css' in rendered)  # Should have custom style sheet
        self.assertTrue('custom-script.js' in rendered)  # Should have custom script

    def test_user_guide_tags_guide_name_filter(self):
        t = Template('{% load user_guide_tags %}{% user_guide guide_name=guide_name %}')
        r = HttpRequest()
        r.user = self.users[0]
        c = Context({
            'request': r,
            'guide_name': 'Test Guide 1'
        })

        # create a guide info
        GuideInfo.objects.create(user=self.users[0], guide=self.guides[1])

        # render the template
        rendered = t.render(c)

        self.assertTrue('<div>Hello test 1!</div>' in rendered)

    def test_user_guide_tags_guide_tag_filter(self):
        t = Template('{% load user_guide_tags %}{% user_guide guide_tags=guide_tags %}')
        r = HttpRequest()
        r.user = self.users[0]
        c = Context({
            'request': r,
            'guide_tags': ['tag0', 'tag1']
        })

        # create a few guide infos
        GuideInfo.objects.create(user=self.users[0], guide=self.guides[0])
        GuideInfo.objects.create(user=self.users[0], guide=self.guides[1])

        # render the template
        rendered = t.render(c)

        self.assertTrue('<div>Hello test 0!</div>' in rendered)
        self.assertTrue('<div>Hello test 1!</div>' in rendered)
