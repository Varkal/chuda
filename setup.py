from setuptools import setup

try:
    with open('README.MD') as readme_file:
        README = readme_file.read()
except FileNotFoundError:
    README = ""

VERSION = '0.0.14'

setup(
    name='chuda',
    packages=['chuda'],
    version=VERSION,
    description='A simple framework to create CLI tools',
    long_description=README,
    license='MIT',
    install_requires=[
        "delegator.py>=0.1.0",
        "argcomplete>=1.9.4",
        "crayons>=0.1.2"
    ],
    author='Romain Moreau',
    author_email='moreau.romain83@gmail.com',
    url='https://github.com/Varkal/chuda',
    download_url='https://github.com/Varkal/chuda/archive/{}.tar.gz'.format(VERSION),
    keywords=['cli', 'chuda'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ],
)
