# -*- coding: utf-8 -*-

import os
import sys
from codecs import open
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)

    def run_tests(self):
        import pytest

        errno = pytest.main([])
        sys.exit(errno)


current_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(os.path.abspath(current_path))


version = {}
with open(
    os.path.join(current_path, "audiolibrix", "version.py"), encoding="utf-8"
) as f:
    exec(f.read(), version)

setup(
    name="audiolibrix",
    version=version["VERSION"],
    description="Audiolibrix Service Bindings for Python",
    long_description=open("./README.md", "r").read(),
    long_description_content_type="text/markdown",
    author="Palo Sopko",
    author_email="pavol@sopko.sk",
    license="MIT",
    keywords="audiolibrix",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["requests >= 2.21.0"],
    tests_require=["pytest >= 6.2.1"],
    cmdclass={"test": PyTest},
    project_urls={
        "Bug Tracker": "https://github.com/palosopko/audiolibrix-python/issues",
        "Source Code": "https://github.com/palosopko/audiolibrix-python",
    },
    python_requires=">=3.6.*",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
