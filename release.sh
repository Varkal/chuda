#!/bin/bash
echo 'release start'
rm -rf dist/
python3 setup.py sdist
twine upload --repository-url https://upload.pypi.org/legacy/ dist/* -u Varkal -p "$(pass pypi)" --verbose
echo 'release end'
