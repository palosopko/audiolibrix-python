import os
import sys
import warnings

from setuptools import setup

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = []

if sys.version_info < (2, 6):
    install_requires.append('requests >= 0.8.8, < 0.10.1')
    install_requires.append('ssl')
else:
    install_requires.append('requests >= 0.8.8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'audiolibrix'))

if sys.version_info < (3, 0):
    try:
        from util import json
    except ImportError:
        install_requires.append('simplejson')

setup(
    name='audiolibrix',
    version='0.1.0',
    description='Audiolibrix service python bindings',
    long_description=open("./README.md", "r").read(),
    author='Palo Sopko',
    author_email='pavol.sopko@backbone.sk',
    url='http://backbone.sk/en/',
    packages=['audiolibrix'],
    install_requires=install_requires,
    use_2to3=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License"
    ])
