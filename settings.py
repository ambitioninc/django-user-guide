import os

import django
from django.conf import settings


def configure_settings():
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
            MIDDLEWARE_CLASSES=(
                'django.middleware.csrf.CsrfViewMiddleware',
            ),
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.admin',
                'user_guide',
                'user_guide.tests',
            ) + (('south',) if django.VERSION[1] <= 6 else ()),
            ROOT_URLCONF='user_guide.urls',
            DEBUG=False,
            USER_GUIDE_SHOW_MAX=5,
            USER_GUIDE_CSS_URL='custom-style.css',
            USER_GUIDE_JS_URL='custom-script.js',
            STATIC_URL='/static/',
            SECRET_KEY='somethignmadeup',
        )
