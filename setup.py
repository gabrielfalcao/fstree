#!/usr/bin/env python

import os
import re
from os.path import dirname, abspath, join
from setuptools import setup, find_packages


local_file = lambda *path: (
    open(join(abspath(dirname(__file__)), *path), 'rb').read())

version_path = local_file('fstree', 'version.py')
version_regex = r"^version\s*=\s*'(.+)'"

found = re.search(version_regex, version_path, re.M)

if not found:
    print version_path, 'does not contain a valid version definition'
    raise SystemExit(1)

package_version = found.group(1)

dependencies = filter(bool, map(bytes.strip, local_file('requirements.txt').splitlines()))

setup(
    name='fstree',
    version=package_version,
    description="\n".join([
        'FSTree - file-system manipulation for python'
    ]),
    entry_points={
        'console_scripts': [
            'fstree = fstree.console.main:entrypoint',
        ],
    },
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='https://github.com/gabrielfalcao/fstree',
    packages=find_packages(exclude=['*tests*']),
    install_requires=dependencies,
    include_package_data=True,
    zip_safe=False,
)
