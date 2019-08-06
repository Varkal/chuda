from setuptools import setup

try:
    with open('README.MD') as readme_file:
        README = readme_file.read()
except FileNotFoundError:
    README = ""

VERSION = '0.1.1'

setup(
    name='chuda',
    packages=['chuda'],
    version=VERSION,
    description='A simple framework to create CLI tools',
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    install_requires=[
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
