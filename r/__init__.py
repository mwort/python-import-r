from types import MethodType
from .module import path

__globals = globals()  # allow globals R package to be loaded


def add_packages():
    from rpy2.robjects.packages import InstalledPackages
    from .package import RPackage

    for p, pth, desc in InstalledPackages():
        __globals[p] = RPackage(p, check_installed=False)


def add_modules():
    import os.path as osp
    from glob import glob
    from .module import path_to_name, RModule

    for d in path:
        for f in glob(osp.join(d, "*.[rR]")):
            __globals[path_to_name(f)] = RModule(f)


def append(self, entry):
    self.appended_paths.append(entry)
    add_modules()
    return


# enable r.path.append() that also reloads modules
path.append = MethodType(append, path)
# add packages, then modules
add_packages()
add_modules()

# activate pandas conversion if pandas is installed
try:
    import pandas
    from .pandas import automatic_pandas_conversion
    automatic_pandas_conversion()
    del pandas, automatic_pandas_conversion
except ModuleNotFoundError:
    pass

del append, MethodType
