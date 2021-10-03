# A Python and commandline interface to R modules and packages

An rpy2 wrapper package to enable Python-style imports of R files and packages
and expose them as commandline tools (based on python-fire) and includes automatic pandas
object conversion.

## Setup
```
pip install import-r
```

## Usage
Import any R installed package or R file in your working dir or on either `$RPYPATH` or `$R_LIBS` paths
like any other python module:
```
    from r import test
    import r.test as rtest
    from r import ggplot2
    import r
    r.path.append('dir/to/my/rfiles')
    from r import my_rfile
```


## Credit
Michel Wortmann < michel.wortmann@ouce.ox.ac.uk >

MIT Licence