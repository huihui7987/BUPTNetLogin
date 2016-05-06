# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

__author__ = 'InG_byr'

setuptools.setup(
    name='BUPTLogin',
    version='0.0.6',
    author='InG_byr',
    author_email='zwkv587@gmail.com',
    description='A Simple login program for bupt net',
    packages=setuptools.find_packages(exclude=['BeautifulSoup4', 'lxml']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bupt.login = BUPTLogin.login:doLogin'
        ]
    },
)
