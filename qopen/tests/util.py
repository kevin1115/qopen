# Copyright 2015-2017 Tom Eulenfeld, MIT license

import contextlib
import os
import shutil
import sys
import tempfile


class _Devnull(object):

    def write(self, _):
        pass


@contextlib.contextmanager
def quiet():
    stdout_save = sys.stdout
    sys.stdout = _Devnull()
    try:
        yield
    finally:
        sys.stdout = stdout_save


def _replace_in_file(fname_src, fname_dest, str_src, str_dest):
    with open(fname_src) as f:
        text = f.read()
    text = text.replace(str_src, str_dest)
    with open(fname_dest, 'w') as f:
        f.write(text)


@contextlib.contextmanager
def tempdir(permanent=False, delete=False):
    if permanent:
        tempdir = os.path.join(tempfile.gettempdir(), 'qopen_test')
        if os.path.exists(tempdir) and delete:
            shutil.rmtree(tempdir)
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)
    else:
        tempdir = tempfile.mkdtemp(prefix='qopen_test_')
    cwd = os.getcwd()
    os.chdir(tempdir)
    # for coverage put .coveragerc config file into tempdir
    # and append correct data_file parameter to config file
    covfn = os.path.join(cwd, '.coverage')
    if not os.path.exists('.coveragerc') and os.path.exists(covfn + 'rc'):
        _replace_in_file(covfn + 'rc', '.coveragerc', '[run]',
                         '[run]\ndata_file = ' + covfn)
    try:
        yield tempdir
    finally:
        os.chdir(cwd)
        if not permanent and os.path.exists(tempdir):
            shutil.rmtree(tempdir)
