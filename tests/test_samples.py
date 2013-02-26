from datetime import datetime as dt
from nose.tools import raises
from pyparsing import ParseException
import os
import pytoml

TOMLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tomlfiles')

def test_toml_files():
    for filename in os.listdir(TOMLS):
        abs = os.path.join(TOMLS, filename)
        if not (os.path.isfile(abs) and abs.endswith(".toml")):
            continue

        def fancy_desc(f):
            f.description = "%s.%s: %s" % (f.__module__, f.__name__, filename)
            return f

        toml = open(abs).read()

        if "invalid" in filename:
            @fancy_desc
            @raises(ParseException, NameError)  # god.
            def check_fail(s):
                pytoml.loads(s)

            yield check_fail, toml

        else:
            expected = eval(open(abs[:-4]+"expected").read())

            @fancy_desc
            def check(s):
                assert pytoml.loads(s) == expected

            yield check, toml
