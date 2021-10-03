import copy

from rpy2.robjects import pandas2ri, numpy2ri
import rpy2.robjects.conversion as conversion
from rpy2.robjects import r


OTHER_DEFAULT_CONVERSIONS = {
    # R (str) : Python type
    "NULL": type(None),
}


def automatic_pandas_conversion(**other_conversions):
    """Automatically convert between pandas and R objects according to rpy2-pandas2ri.

    This is based on the pandas2ri.activate function that will be deprected soon.

    Arguements
    ----------
    **other_conversions : str : object
        Additional conversion of python objects from/to R given as
        R code (str): Python object.
    """
    other_conversions = copy.deepcopy(OTHER_DEFAULT_CONVERSIONS)
    other_conversions.update(other_conversions)

    new_converter = conversion.Converter('snapshot before pandas conversion',
                                         template=conversion.converter)

    npc, pdc = numpy2ri.py2rpy.registry.items(), pandas2ri.py2rpy.registry.items()
    for k, v in list(npc) + list(pdc):
        if k is object:
            continue
        new_converter.py2rpy.register(k, v)
    # other conversions
    for rcode, p in other_conversions.items():
        new_converter.py2rpy.register(p, lambda x: r(rcode))

    npc, pdc = numpy2ri.rpy2py.registry.items(), pandas2ri.rpy2py.registry.items()
    for k, v in list(npc) + list(pdc):
        if k is object:
            continue
        new_converter.rpy2py.register(k, v)
    # other conversions
    for rcode, p in other_conversions.items():
        new_converter.rpy2py.register(r(rcode), lambda x: p)

    conversion.set_conversion(new_converter)
    return
