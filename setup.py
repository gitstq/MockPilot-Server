#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MockPilot-CLI Setup Script
"""

from setuptools import setup, find_packages
import os

# Read README
readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
long_description = ''
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='mockpilot-cli',
    version='1.0.0',
    author='MockPilot Team',
    author_email='mockpilot@example.com',
    description='Lightweight Terminal API Mock Server Intelligent Engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitstq/MockPilot-CLI',
    py_modules=['mockpilot'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Mocking',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'mockpilot=mockpilot:main',
        ],
    },
    keywords='mock api server cli terminal http rest testing development',
    project_urls={
        'Bug Reports': 'https://github.com/gitstq/MockPilot-CLI/issues',
        'Source': 'https://github.com/gitstq/MockPilot-CLI',
    },
)
