from __future__ import with_statement
from dill.dill import PY3, check

from dill.temp import capture

import sys


#FIXME: this doesn't catch output... it's from the internal call
def _bla(func, **kwds):
    try:
        with capture('stdout') as out:
            check(func, **kwds)
    except Exception:
        e = sys.exc_info()[1]
        raise AssertionError(str(e))
    else:
        assert 'Traceback' not in out.getvalue()
    finally:
        out.close()



def test_lambda():
    f = lambda x:x**2
    _bla(f)
    _bla(f, recurse=True)
    _bla(f, byref=True)
    _bla(f, protocol=0)
    #TODO: test incompatible versions
    # SyntaxError: invalid syntax
    if PY3:
        _bla(f, python='python3.4')
    else:
        _bla(f, python='python2.7')
    #TODO: test dump failure
    #TODO: test load failure


# EOF
