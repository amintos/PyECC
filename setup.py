#!/usr/bin/python2.4
#
# Copyright 2007 The Python-Twitter Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# copied from https://github.com/bear/python-twitter/blob/master/setup.py
#

'''The setup and build script for the python-twitter library.'''

__author__ = 'niccokunzmann@aol.com'
__version__ = '0.0.1'


# The base package metadata to be used by both distutils and setuptools
METADATA = dict(
    name = "distacc",
    version = __version__,
    packages = ['ecc'],
    author='Toni Mattis',
    author_email='solaris@live.de',
    description='Distributed object access',
    license='MIT',
    url='https://github.com/niccokunzmann/distacc',
    keywords='distributed game programming',
)

# Extra package metadata to be used only if setuptools is installed
SETUPTOOLS_METADATA = dict(
    install_requires = ['setuptools', 'simplejson', 'oauth2', 'python-twitter', \
                        'bson'],
    include_package_data = True,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications',
        'Topic :: Games/Entertainment', 
        'Topic :: Internet',
        'Topic :: Software Development :: Object Brokering', 
    ],
##    test_suite = 'distacc_test',
)


def Read(file):
    return open(file).read()

def BuildLongDescription():
    return '\n'.join([Read('README.md'), ])

def Main():
    # Build the long_description from the README and CHANGES
    METADATA['long_description'] = BuildLongDescription()

    # Use setuptools if available, otherwise fallback and use distutils
    try:
        import setuptools
        METADATA.update(SETUPTOOLS_METADATA)
        setuptools.setup(**METADATA)
    except ImportError:
        import distutils.core
        distutils.core.setup(**METADATA)


if __name__ == '__main__':
    Main()
