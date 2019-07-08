# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os


def version():
    cdir = os.path.dirname(__file__)
    VERSION = open(os.path.join(cdir, "VERSION")).read().strip("\n")
    return VERSION


# Compute requirements
cdir = os.path.dirname(__file__)
requirements = open(os.path.join(cdir, "requirements.txt")).read()


setup(
    name="onna-jello",
    version=version(),
    description="",
    long_description="",
    keywords=["atlasense"],
    author="Spyder Team",
    author_email="spyder@onna.com",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    url="",
    license="Private",
    zip_safe=True,
    include_package_data=True,
    package_data={"": ["*.txt", "*.rst"]},
    packages=find_packages(),
    install_requires=requirements,
)
