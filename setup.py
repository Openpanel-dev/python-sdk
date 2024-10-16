from setuptools import setup, find_packages

setup(
    name="openpanel",
    version="0.0.1",
    author="OpenPanel",
    author_email="hello@openpanel.dev",
    description="OpenPanel SDK for Python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Openpanel-dev/python-sdk",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests>=2.28.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    license='AGPL-3.0-or-later',
)