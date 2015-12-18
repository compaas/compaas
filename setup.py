from setuptools import setup, find_packages
import os


packagename = 'compaas'
description = 'Publishing tool for CoMPASS - ' \
              'Conference & Meeting Proceedings of the AAS'
author = 'Jonathan Sick'
author_email = 'jsick@lsst.org'
license = 'MIT'
url = 'https://github.com/jonathansick/compaas'
version = '0.1.0.dev0'


def read(filename):
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return open(full_filename).read()

long_description = read('README.rst')


setup(
    name=packagename,
    version=version,
    description=description,
    long_description=long_description,
    url=url,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='aas',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['future', 'requests', 'xmltodict'],
    tests_require=['pytest'],
    # package_data={},
)
