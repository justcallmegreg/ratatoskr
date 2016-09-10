from setuptools import setup, find_packages
from os import path
from pip.req import parse_requirements

here = path.abspath(path.dirname(__file__))

version_file = open(path.join(here, 'VERSION'))

PROJECT_URL = 'http://github.com/ngergo/ratatoskr'
VERSION = version_file.read().strip()

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
    description='TODO',
    url=PROJECT_URL,
    download_url=PROJECT_URL + '/tarball/' + VERSION,
    author='Gergo Nagy',
    author_email='grigori.grant@gmail.com',
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
