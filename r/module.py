import os
import os.path as osp
import glob
import re

from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage


class SearchPath:
    """Dynamic search path class that allows adding paths after package is imported.
    Search order:
    -------------
    1) . (working dir)
    2) paths added via r.path.append
    3) environment variables
    """
    env_variables = ['R_LIBS', 'RPYPATH']
    appended_paths = []

    def append(self, entry):
        """Will be overridden in r.__init__ to reload modules at package level."""
        pass

    def __iter__(self):
        envv_paths = [
            p for v in self.env_variables
            for p in os.environ.get(v, '').split(':')
        ]
        for p in ['.'] + self.appended_paths + envv_paths:
            yield p


path = SearchPath()


def path_to_name(path):
    """Convert a filepath to a valid python variable name."""
    filename = osp.splitext(osp.basename(path))[0]
    return re.sub(r'\W|^(?=\d)', '_', filename)


def find_r_file(name):
    name = path_to_name(name)
    # first check for unconverted names (fast)
    for d in path:
        pth = osp.join(d, name)
        if osp.exists(pth+'.r'):
            return pth + '.r'
        if osp.exists(name+'.R'):
            return name+'.R'
    # check for converted names (slower)
    for d in path:
        files = {path_to_name(f): f for f in glob.glob(osp.join(d, "*.[rR]"))}
        if name in files:
            return files[name]
    # if not found
    return None


class RModule(SignatureTranslatedAnonymousPackage):
    """An R module class that is initialised only on first use of method/attribute."""
    def __init__(self, module_or_path):
        if osp.exists(module_or_path):
            self.__file__ = module_or_path
        else:
            self.__file__ = find_r_file(module_or_path)
            if self.__file__ is None:
                raise ImportError(f'Cant find {module_or_path} in {path}')
        self.__name__ = path_to_name(self.__file__)
        self._is_initialised = False
        return

    def __getattr__(self, key):
        # initialise if not yet
        if not self._is_initialised:
            self._initialise()
        # in all other instances
        if key in self.__dict__:
            return self.__dict__[key]
        else:
            raise AttributeError(key)

    def _initialise(self):
        with open(self.__file__) as f:
            rcode = f.read()
        SignatureTranslatedAnonymousPackage.__init__(self, rcode, self.__name__)
        self._is_initialised = True
        return
