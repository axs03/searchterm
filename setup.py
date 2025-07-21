#!/usr/bin/env python3

from setuptools import setup, find_packages
from searchterm import __version__ # prevent circular import

setup(
    name="searchterm",
    version=__version__,
    description="command-line question-answering model",
    author="Aman Sahu",
    author_email="axs03@github.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "gpt4all",
        "configparser",
        "click>=8.0.0"
    ],
    entry_points={
        "console_scripts": [
            "st=searchterm.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "searchterm": ["config.ini"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
