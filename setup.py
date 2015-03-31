#!/usr/bin/env python
import codecs
import setuptools
import sys

from arbitrator import __version__


def read_requirements_file(name):
    try:
        with open(name) as req_file:
            return [line[0:line.index('#')] if '#' in line else line
                    for line in req_file]
    except IOError:
        pass


install_requirements = read_requirements_file('requirements.txt')
test_requirements = read_requirements_file('test-requirements.txt')

with codecs.open('README.rst', 'rb', encoding='utf-8') as readme:
    long_description = '\n' + readme.read()


setuptools.setup(
    name='arbitrator',
    version=__version__,
    author='Dan Tracy',
    author_email='djt5019@gmail.com',
    url='http://github.com/djt5019/arbitrator',
    description='Handles content type negotation in Tornado',
    long_description=long_description,
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    zip_safe=True,
    platforms='any',
    install_requires=install_requirements,
    test_suite='nose.collector',
    tests_require=test_requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
    ],
)
