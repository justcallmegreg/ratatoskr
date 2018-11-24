from setuptools import setup, find_packages
from os import path
try: # for pip >= 10
  from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
  from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

version_file = open(path.join(here, 'VERSION'))

PROJECT_URL = 'http://github.com/ngergo/ratatoskr'
VERSION = version_file.read().strip()

DESCRIPTION = """
Ratatoskr is a library written in Python to make the development of AWS Lambdas easier and more secure.
It supports implementing "singleshot" operations that can be reached from an AWS Lambda function and
validating the input parameters to avoid unnecessary boilerplate for argument checking.
"""

install_reqs = parse_requirements(
    path.join(here, 'requirements.txt'),
    session=False
)
install_requirements = [str(ir.req) for ir in install_reqs]

dev_reqs = parse_requirements(
    path.join(here, 'requirements.txt'),
    session=False
)
development_requirements = [str(ir.req) for ir in dev_reqs]

setup(
    name='ratatoskr',
    version=VERSION,
    description=DESCRIPTION,
    url=PROJECT_URL,
    download_url=PROJECT_URL + '/tarball/v' + VERSION,
    author='Gergo Nagy',
    author_email='contact@gergonagy.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
    ],
    keywords='aws lambda development ratatoskr microservice amazon',
    packages=find_packages(),
    install_requires=install_requirements,
    extras_require={
        'dev': development_requirements
    },
)
