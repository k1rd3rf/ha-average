#!/usr/bin/env python

import io
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    # Code from here:
    # https://docs.pytest.org/en/latest/goodpractices.html#manual-integration

    def finalize_options(self):
        TestCommand.finalize_options(self)
        # we don't run integration tests which need an actual Beward device
        self.test_args = ['-m', 'not integration']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import shlex

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


src = io.open('custom_components/average/__init__.py', encoding='utf-8').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", src))
docstrings = re.findall('"""(.*?)"""', src, re.MULTILINE | re.DOTALL)

NAME = 'average'

PACKAGES = find_packages(exclude=['tests', 'tests.*']),

AUTHOR_EMAIL = metadata['author']
VERSION = metadata['version']
WEBSITE = metadata['website']
LICENSE = metadata['license']
DESCRIPTION = docstrings[0]

# Extract name and e-mail ("Firstname Lastname <mail@example.org>")
AUTHOR, EMAIL = re.match(r'(.*) <(.*)>', AUTHOR_EMAIL).groups()

REQUIREMENTS = list(open('requirements.txt'))
TEST_REQUIREMENTS = list(open('requirements_test.txt'))

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    url=WEBSITE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='tests'
)
