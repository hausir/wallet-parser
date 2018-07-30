# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

VERSION = '0.0.2'

setup(
    name='wallet-parser',
    version=VERSION,
    license='MIT',
    description='parse wallet.dat file to get addresses',
    url='https://github.com/hausir/wallet-parser',
    author='hausir',
    author_email='hausir@icloud.com',
    platforms='any',
    install_requires=[
        'bsddb3>=6.2.5',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wallet-parser=wallet_parser.cli:main',
        ],
    },
)
