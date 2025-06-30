#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="searchterm",
    version="1.0.0",
    description="A command-line AI chat application",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "gpt4all",
        "configparser",
    ],
    entry_points={
        "console_scripts": [
            "searchterm=searchterm.cli:main",
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
