import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ya-tasks',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='Private',
    description='Homework :)',
    long_description=README,
    url='https://www.example.com/',
    author='Sergey I',
    author_email='yourname@example.com',
    install_requires=[
        'jsonschema==2.6.0'
    ],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
    ],
)