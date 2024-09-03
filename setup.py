from setuptools import setup, find_packages

setup(
    name="openpanel",
    version="0.0.1",
    author="OpenPanel",
    author_email="support@openpanel.com",
    description="OpenPannel SDK for Python",
    long_description_content_type="text/markdown",
    url="https://github.com/openpannel/python-sdk",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "requests>=2.28.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)