# -*- coding: UTF-8 -*-
"""
Setup
"""
import re
import sys
import os
from setuptools import setup

NAME = "razortrace"


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    path = os.path.join(package, "__init__.py")
    init_py = open(path, "r", encoding="utf8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)  # noqa


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


URL = "https://github.com/manbehindthemadness/razortrace"
DESCRIPTION = "Straight forward memory leak detection"
LONG_DESCRIPTION = \
"""
Long description here
"""


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported')

install_requires = [
    "Pillow >= 8",
    "pytest",
    "sphinx",
]

setup(
    name="razortrace",
    version=get_version("razortrace"),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords="malloc, memory, leak, trace",
    author="manbehindthemadness",
    author_email="manbehindthemadness@gmail.com",
    url=URL,
    license="MIT",
    packages=get_packages('razortrace'),
    install_requires=install_requires,
    include_package_data=True,
    # package_data={'razortrace': ['defaults.ini', 'err.png']}
)
