#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from djangocms_icon import __version__


REQUIREMENTS = [
    'django-cms>=3.4.5',
    'djangocms-attributes-field>=0.4.0',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.0',
    'Framework :: Django :: 2.1',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    name='js-icon',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.com',
    url='https://github.com/divio/djangocms-icon',
    license='BSD',
    description='Adds icon plugin to django CMS.',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
