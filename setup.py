"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import os
import re
# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))


def get_requires(filename):
    requirements = []
    with open(filename, "rt") as req_file:
        for line in req_file.read().splitlines():
            if not line.strip().startswith("#"):
                requirements.append(line)
    return requirements


project_requirements = get_requires("artifactory_du/requirements.txt")


def load_version():
    """
    Loads a file content'''
    :return:
    """
    filename = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "artifactory_du", "version.py"))
    with open(filename, "rt") as version_file:
        artifactory_du_init = version_file.read()
        version = re.search("__version__ = '([0-9a-z.-]+)'", artifactory_du_init).group(1)
        return version


# def generate_long_description_file():
#     import pypandoc
#
#     output = pypandoc.convert('README.md', 'rst')
#     return output

LONG_DESCRIPTION = """artifactory-du is used in the same manner as original du from *nix, although launch options are different. 

See artifactory-du –help for details.

`https://devopshq.github.io/artifactory-du/ <https://devopshq.github.io/artifactory-du/>`_
"""

setup(
    name='artifactory-du',
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=load_version(),  # + ".rc1",

    description='Artifactory Disk Usage command line interface (artifactory-du)',
    long_description=LONG_DESCRIPTION,
    # long_description=generate_long_description_file(),

    # The project's main homepage.
    url='https://devopshq.github.io/artifactory-du',

    # Author details
    author='DevOpsHQ',
    author_email='allburov@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords=['disk', 'usage', 'artifactory', 'jfrog', 'devopshq', ],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=project_requirements,

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': dev_requirements,
    # },
    setup_requires=[
        'pytest-runner',
        'pytest',
    ],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'artifactory_du': ['*.txt'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'artifactory_du=artifactory_du.artifactory_du:main',
            'artifactory-du=artifactory_du.artifactory_du:main',
        ],
    },
)
