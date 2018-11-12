#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import cryptapi

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(

    name='django-cryptapi',

    version=cryptapi.__version__,

    packages=find_packages(),

    author="CryptAPI",

    author_email="cryptapi@protonmail.com",
    install_requires=[
        'django',
        'requests'
    ],
    description="Django implementation of CryptAPI's payment gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",

    include_package_data=True,

    url='https://github.com/cryptapi/django-cryptapi',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],

    license="MIT",

    zip_safe=False
)
