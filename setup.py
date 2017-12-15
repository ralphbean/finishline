#!/usr/bin/env python
"""
Install script.
"""

from pip.req import parse_requirements

from setuptools import setup

install_requirements = parse_requirements('requirements.txt', session=False)

setup(
    name='finishline',
    version='0.0.0',
    description='A script for generating reports from JIRA',
    author="Ralph Bean <rbean@redhat.com>",
    url='https://github.com/ralphbean/finishline',
    # license="",
    install_requires=[str(r.req) for r in install_requirements],
    scripts=['finishline']
)
