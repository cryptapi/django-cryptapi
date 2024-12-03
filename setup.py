#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-cryptapi',
    version='0.4.6',
    packages=find_packages(exclude=['django_store']),
    author="CryptAPI",
    author_email="info@cryptapi.io",
    install_requires=[
        'django',
        'requests',
    ],
    description="Django implementation of CryptAPI's payment gateway",
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
    url='https://github.com/cryptapi/django-cryptapi',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    zip_safe=False,
)
