#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import os, pkg_resources

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    str(requirement)
    for requirement in pkg_resources.parse_requirements(
        open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
    )
]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Ye Yu",
    author_email='rafolwen98@gmail.com',
    python_requires='>=3.6,<3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Another Audio API - Collection of audio and music processing API with massive amount of dependencies",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='aaapi',
    name='aaapi',
    packages=find_packages(include=['aaapi', 'aaapi.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ye-yu/aaapi',
    version='0.1.1',
    zip_safe=False,
)
