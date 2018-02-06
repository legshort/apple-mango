import os
import sys

from setuptools import setup

setup(
    name='mango',
    version='0.1',
    url='https://github.com/legshort/mango/',
    license='MIT',
    author='Jun Young Lee',
    author_email='legshort@gmail.com',
    description='Light weight BDD Pattern',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    keywords=['tdd', 'bdd', 'test'],
    packages=['mango'],
    install_requires=[
        'wrapt>=1.10.0',
    ],
    long_description=open('README.md').read(),
)
