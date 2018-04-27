""" Packaging settings. """

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup
import setuptools.command.test

from find_store import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name = 'find_store',
    version = __version__,
    description = 'A command line program for finding stores.',
    long_description = long_description,
    url = 'https://github.com/srslafazan/find-store',
    author = 'Shain Lafazan',
    author_email = 'shain.codes@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt'],
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points = {
        'console_scripts': [
            'find_store=find_store.cli:main',
        ],
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
