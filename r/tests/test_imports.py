
R_MODULE = """
test <- function(i) {
    return (i * i)
}
test_frame <- function() {
    return (data.frame(e=c(1, 2, 3)))
}
"""


def create_test_module(tmp_path):
    f = tmp_path / "test_module.r"
    f.write_text(R_MODULE)
    # add to path
    import r
    r.path.append(str(tmp_path))
    return


def test_module_import(tmp_path):
    create_test_module(tmp_path)
    from r import test_module
    assert hasattr(test_module, 'test')
    assert test_module.test(2) == 4


def test_package_import():
    from r import base
    assert hasattr(base, 'factor')


def test_pandas_conversion(tmp_path):
    create_test_module(tmp_path)
    from r import test_module
    assert hasattr(test_module, 'test_frame')
    from pandas import DataFrame
    assert type(test_module.test_frame()) is DataFrame


def test_cli(tmp_path):
    import os.path as osp
    import subprocess as sp
    create_test_module(tmp_path)
    rcli = ['rcli', str(tmp_path/'test_module.r')]
    out = sp.check_output(rcli + ['test', '--i=2'])
    assert out.decode().strip() == '[4]'
    csvfile = str(tmp_path/'tmp.csv')
    out = sp.check_output(rcli + ['test_frame', '-', 'to-csv', csvfile])
    assert osp.exists(csvfile)
