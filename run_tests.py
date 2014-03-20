"""
Provides the ability to run test on a standalone Django app.
"""
import os
import sys
from django.conf import settings
from optparse import OptionParser


if not settings.configured:
    # Determine the database settings depending on if a test_db var is set in CI mode or not
    test_db = os.environ.get('DB', None)
    if test_db is None:
        db_config = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ambition_dev',
            'USER': 'ambition_dev',
            'PASSWORD': 'ambition_dev',
            'HOST': 'localhost'
        }
    elif test_db == 'postgres':
        db_config = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'user_guide',
        }
    else:
        raise RuntimeError('Unsupported test DB {0}'.format(test_db))

    settings.configure(
        DATABASES={
            'default': db_config,
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'south',
            'user_guide',
            'user_guide.tests',
        ),
        ROOT_URLCONF='user_guide.urls',
        DEBUG=False,
        USER_GUIDE_HTML_MAX=256,
        USER_GUIDE_TAG_MAX=256,
        USER_GUIDE_SHOW_MAX=5,
        USER_GUIDE_CSS_URL='custom-style.css',
        USER_GUIDE_JS_URL='custom-script.js',
        STATIC_URL='/collectstatic/'
    )

from django_nose import NoseTestSuiteRunner


def run_tests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['user_guide']

    kwargs.setdefault('interactive', False)

    test_runner = NoseTestSuiteRunner(**kwargs)

    failures = test_runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--verbosity', dest='verbosity', action='store', default=1, type=int)
    parser.add_options(NoseTestSuiteRunner.options)
    (options, args) = parser.parse_args()

    run_tests(*args, **options.__dict__)
