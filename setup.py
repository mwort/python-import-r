# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages
from datetime import date


__author__ = "Michel Wortmann"
__copyright__ = "Copyright %s, " % date.today().year + __author__
__version__ = '0.2'
__email__ = "michel.wortmann@ouce.ox.ac.uk"
__license__ = "MIT"
__url__ = "https://github.com/mwort/python-import-r"

requirements = [
    "rpy2==3.4.*",
]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Topic :: Scientific/Engineering",
]

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name="import-r",
      version=__version__,
      author=__author__,
      author_email=__email__,
      url=__url__,
      packages=find_packages(),
      install_requires=requirements,
      description="Enables importing R packages and files (like python modules) in python syntax via rpy2.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      license=__license__,
      classifiers=classifiers,
      python_requires=">=3.5",
      entry_points={'console_scripts': ['rcli = r.__main__:_rcli']},
      extras_require={
        'rcli':  ["fire"],
        'test': ['pytest', 'pandas', 'fire', 'twine'],
        },
      )
