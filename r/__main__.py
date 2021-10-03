#!/usr/bin/env python
"""
This file enables the python-fire based commandline interface.
"""
from .module import RModule
from .package import RPackage


def rcli(path_module_or_package):
    """Commandline interface to R packages and functions in a file.

    Examples:
    ---------
    # with a package
    rcli utils install_packages ggplot2
    # with a file
    rcli path/test.r some_function
    """
    try:
        cmp = RModule(path_module_or_package)
    except ImportError:
        try:
            cmp = RPackage(path_module_or_package)
        except ImportError:
            raise ImportError(f'{path_module_or_package} not found.')
    # needs to be initialised to work with fire
    cmp._initialise()
    return cmp


def _rcli():
    try:
        from fire import Fire
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            'The commandline interface requires python-fire. (pip install fire)'
        )
    Fire(rcli)
    return


if __name__ == "__main__":
    _rcli()
