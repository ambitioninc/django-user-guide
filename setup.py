# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'user_guide/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='django-user-guide',
    version=get_version(),
    description='Show configurable HTML guides to users.',
    long_description=open('README.md').read(),
    url='https://github.com/ambitioninc/django-user-guide',
    author='Jeff McRiffey',
    author_email='jeff.mcriffey@ambition.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7'
    ],
    license='MIT',
    install_requires=[
        'Django>=1.6',
    ],
    tests_require=[
        'psycopg2',
        'django-nose',
        'django-dynamic-fixture',
        'south>=1.0.2',
        'freezegun'
    ],
    test_suite='run_tests.run_tests',
    include_package_data=True,
)
