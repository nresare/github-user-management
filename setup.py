#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2016 Lynn Root
import io
import os
import re
from setuptools import setup, find_packages

NAME = "github-user-management"
META_PATH = os.path.join("github_user_management", "__init__.py")
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for fl in filenames:
        with io.open(fl, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


def install_requires(filename="requirements.txt"):
    """
    Read requirements from requirements.txt file w/i same directory.
    """
    raw_reqs_string = read(filename)
    reqs_string = raw_reqs_string.strip()
    reqs_list = reqs_string.split("\n")
    return [r for r in reqs_list if not r.startswith("#")]

setup(
    name=NAME,
    version=find_meta("version"),
    description=find_meta("description"),
    url=find_meta("uri"),
    license=find_meta("license"),
    author=find_meta("author"),
    author_email=find_meta("email"),
    keywords=["github", "ldap"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ghmanage = github_user_management.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=install_requires(),
)
