from setuptools import find_packages, setup

import ds

setup(
    name='ds',
    packages=find_packages(include=['ds']),
    version='0.1.0',
    description='File-based Key Value DataStore Library',
    author='Johnitto Francis',
    license='MIT',
    install_requires=[],
    test_suite='tests'
)