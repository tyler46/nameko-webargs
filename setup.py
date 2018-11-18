#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    name='nameko_webargs',
    version='0.1.0',
    author="Spyros Markopoulos",
    author_email='mail.doctor46@gmail.com',
    url='https://github.com/tyler46/nameko_webargs',
    license="MIT license",
    description="Nameko integration with Webargs",
    long_description=readme + '\n\n' + history,
    python_requires='>=3.5',
    install_requires=[
        "nameko>=2.11.0",
        "webargs>=4.1.2"
    ],
    extras_require={
        'test': [
            "pytest>=3.8",
            "coverage>=4.5",
            "pytest-cov>=2.6",
            "tox>=3.3",
            "codecov>=2.0",
        ],
    },
    setup_requires=[
        "pytest-runner",
    ],
    packages=find_packages(include=['nameko_webargs']),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    keywords='nameko_webargs',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
