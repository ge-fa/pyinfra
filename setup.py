# pyinfra
# File: setup.py
# Desc: pyinfra package setup

import sys

try:
    from setuptools import setup, find_packages

except ImportError:
    print('''
Error: pyinfra needs setuptools in order to install:

using pip: pip install setuptools
using a package manager (apt, yum, etc), normally named: python-setuptools
    '''.strip())

    sys.exit(1)


INSTALL_REQUIRES = (
    'gevent>1,<2',
    'paramiko>1,<3',
    'click>2',
    'docopt<1',
    'colorama<1',
    'jinja2>2,<3',
    'python-dateutil>2,<3',
    'six>1,<2',
    'setuptools',
)

TEST_REQUIRES = (
    'nose==1.3.7',
    'jsontest==1.3',
    'coverage==4.4.1',
    'mock==1.3.0',
)

DEV_REQUIRES = TEST_REQUIRES + (
    # Releasing
    'wheel',
    'twine==1.9.1',

    # Dev debugging
    'ipdb==0.10.3',
    'ipdbplugin==1.4.5',

    # Dev docs requirements
    'sphinx==1.6.2',
    'sphinx-autobuild==0.6.0',
    'sphinx-better-theme==0.13',

    # Convert markdowns to rst for long_description
    'pypandoc==1.4',
)


# Extract version info without importing entire pyinfra package
version_data = {}
with open('pyinfra/version.py') as f:
    exec(f.read(), version_data)


# Get the long_description from the README, hopefully as rst
long_description = open('README.md', 'r').read()

try:
    from pypandoc import convert_text

    # Strip out the example image because pypi's RST processing ignores width
    long_description = '\n'.join(
        line for line in long_description.split('\n')
        if line not in (
            'When you run pyinfra you\'ll see something like:',
            '![](https://raw.githubusercontent.com/Fizzadar/pyinfra/develop/docs/example_deploy.png)',
        )
    )

    long_description = convert_text(long_description, 'rst', 'markdown')

except (ImportError, OSError):
    # Ignore this - release.sh checks for making releases
    pass


if __name__ == '__main__':
    setup(
        version=version_data['__version__'],
        name='pyinfra',
        description='Deploy stuff by diff-ing the state you want against the remote server.',
        long_description=long_description,
        author='Nick / Fizzadar',
        author_email='pointlessrambler@gmail.com',
        license='MIT',
        url='http://github.com/Fizzadar/pyinfra',
        packages=find_packages(),
        entry_points={
            'console_scripts': (
                'pyinfra=pyinfra_cli.__main__:execute_pyinfra',
            ),
        },
        install_requires=INSTALL_REQUIRES,
        extras_require={
            'dev': DEV_REQUIRES,
            'test': TEST_REQUIRES,
        },
        classifiers=(
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Topic :: System :: Systems Administration',
        ),
    )
