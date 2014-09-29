# import multiprocessing to avoid this bug (http://bugs.python.org/issue15881#msg170215)
import multiprocessing
assert multiprocessing
import re
from setuptools import setup, find_packages


def get_version():
    """
    Extracts the version number from the version.py file.
    """
    VERSION_FILE = 'entity_subscription/version.py'
    mo = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', open(VERSION_FILE, 'rt').read(), re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError('Unable to find version string in {0}.'.format(VERSION_FILE))


setup(
    name='django-entity-subscription',
    version=get_version(),
    description='Make subscription management easy and entity-based.',
    long_description=open('README.rst').read(),
    url='https://github.com/ambitioninc/django-entity-subscription',
    author='Erik Swanson',
    author_email='opensource@ambition.com',
    keywords='',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
    license='MIT',
    install_requires=[
        'django>=1.6,<1.7',
        'django-entity>=1.0',
    ],
    tests_require=[
        'django-dynamic-fixture ',
        'django-nose',
        'south',
        'mock',
    ],
    test_suite='run_tests.run_tests',
    include_package_data=True,
    zip_safe=False,
)
