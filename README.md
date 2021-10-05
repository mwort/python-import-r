# Python-style imports of R files and packages

An rpy2 wrapper package to enable Python-style imports of R files and packages
and expose them as commandline tools (based on python-fire), including automatic pandas
object conversion if it is installed.

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
### Commandline interface
Install with cli support (`pip install import-r[rcli]`) and then use R files and packages on the commandline
like this:
```
    rcli utils install_packages ggplot2
    rcli path/to/my/rfile.R function1 --arg=2 --flag
```

### Test and release
```
pip install .[test]
pytest
python setup.py sdist
twine upload dist/*
```
Once everything passed successfully, tag and push to github:
```
version=0.1
git commit -m "Release v${version}"
git tag "v$version"
git push; git push --tags
```

## Credit
Michel Wortmann <michel.wortmann@ouce.ox.ac.uk>

MIT Licence
