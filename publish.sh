#!/bin/bash

python3 -m venv venv
source venv/bin/activate

echo "Upgrading setuptools, wheel, and twine..."
python3 -m pip install --upgrade setuptools wheel twine

echo
echo "Cleaning up old distribution files..."
rm -rf dist

echo
echo "Building distribution files..."
python3 setup.py sdist bdist_wheel

echo
echo "Uploading package to PyPI..."
python3 -m twine upload dist/*

echo
echo "Process completed. Please check the output for any errors."
