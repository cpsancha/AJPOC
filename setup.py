from os import path, getcwd
from setuptools import setup, find_packages
from AJPOC import __author__ as ajpoc_author
from AJPOC import __version__ as ajpoc_version

with open(path.join(path.realpath(path.join(getcwd(), path.dirname(__file__))), "README.rst"), "r") as fh:
    long_description = fh.read()

setup(
    name="AJPOC",
    version=ajpoc_version,
    author=ajpoc_author,
    author_email="sork93@gmail.com",
    description="Customizable web crawler for the Airbus job portal",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sork93/AJPOC",
    packages=find_packages(),
    package_data={'': ['*.png']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
