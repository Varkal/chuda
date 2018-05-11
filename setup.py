from distutils.core import setup
setup(
    name='chuda',
    packages=['chuda'], # this must be the same as the name above
    version='0.0.1',
    description='A simple framework to create CLI tools',
    license='MIT',
    install_requires=[
        "delegator.py>=0.1.0",
        "argcomplete>=1.9.4",
    ],
    author='Romain Moreau',
    author_email='moreau.romain83@gmail.com',
    url='https://github.com/Varkal/chuda', # use the URL to the github repo
    download_url='https://github.com/Varkal/chuda/archive/0.0.1.tar.gz', # I'll explain this in a second
    keywords=['cli'], # arbitrary keywords
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Programming Language :: Python :: 3"
    ],
)
