from rpy2.robjects.packages import InstalledPackages, InstalledSTPackage
import rpy2.rinterface as rinterface


class RPackage(InstalledSTPackage):
    """An R package class that is initialised only on first use of method/attribute."""
    def __init__(self, name, check_installed=True):
        self.__name__ = name
        if check_installed:
            msg = f'Package {name} not installed.'
            if not InstalledPackages().isinstalled(name):
                raise ImportError(msg)
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
        """Initialise package (duplicated from rpy2.robjects.packages.rimport)."""
        _as_env = rinterface.baseenv['as.environment']
        _package_has_namespace = rinterface.baseenv['packageHasNamespace']
        _system_file = rinterface.baseenv['system.file']
        _get_namespace = rinterface.baseenv['getNamespace']
        _get_namespace_version = rinterface.baseenv['getNamespaceVersion']
        _get_namespace_exports = rinterface.baseenv['getNamespaceExports']
        if _package_has_namespace(self.__name__,
                                  _system_file(package=self.__name__)):
            env = _get_namespace(self.__name__)
            version = _get_namespace_version(self.__name__)[0]
            exported_names = set(_get_namespace_exports(self.__name__))
        else:
            env = _as_env(rinterface.StrSexpVector(['package:'+self.__name__]))
            exported_names = None
            version = None
        InstalledSTPackage.__init__(
            self, env, self.__name__,
            exported_names=exported_names,
            version=version,
        )
        self._is_initialised = True
        return
