import os.path
from datetime import datetime as dt
from nose.tools import raises
from pyparsing import ParseException
import pytoml

TOMLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tomlfiles')

# Datetimes
def test_datetime_basic():
    expected =  {
        'dob': dt.strptime("1982-10-22T23:59:00Z", pytoml.TOMLParser.ISO8601)
    }
    with open(os.path.join(TOMLS, 'datetime', 'datetime-basic.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

@raises(ParseException)
def test_datetime_invalid1():
    with open(os.path.join(TOMLS, 'datetime', 'invalid-datetime1.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_datetime_invalid2():
    with open(os.path.join(TOMLS, 'datetime', 'invalid-datetime2.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_datetime_invalid3():
    with open(os.path.join(TOMLS, 'datetime', 'invalid-datetime3.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_datetime_invalid4():
    with open(os.path.join(TOMLS, 'datetime', 'invalid-datetime4.toml')) as f:
        pytoml.loads(f.read())


# Booleans
def test_bool_basic():
    expected = {'enabled': True}
    with open(os.path.join(TOMLS, 'bool', 'bool-basic.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

@raises(ParseException)
def test_bool_invalid1():
    with open(os.path.join(TOMLS, 'bool', 'invalid-boolean1.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_bool_invalid2():
    with open(os.path.join(TOMLS, 'bool', 'invalid-boolean2.toml')) as f:
        pytoml.loads(f.read())


# Comments
def test_comments():
    with open(os.path.join(TOMLS, 'comments', 'comment-basic.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == {}


# Floats
def test_float_basic():
    expected = {'pi': 3.1415}
    with open(os.path.join(TOMLS, 'float', 'float-basic.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

@raises(ParseException)
def test_float_invalid1():
    with open(os.path.join(TOMLS, 'float', 'float-invalid1.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_float_invalid2():
    with open(os.path.join(TOMLS, 'float', 'float-invalid2.toml')) as f:
        pytoml.loads(f.read())


# Integers
def test_int_basic():
    expected = {'connection_max': 5000}
    with open(os.path.join(TOMLS, 'int', 'int-basic.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected


# Strings
def test_string_basic1():
    expected = {'ip': '10.0.0.2'}
    with open(os.path.join(TOMLS, 'string', 'string-basic1.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

def test_string_basic2():
    expected = {'quote': "I'm a string. \"You can quote me\". Tab \t newline \n you get it."}
    with open(os.path.join(TOMLS, 'string', 'string-basic2.toml')) as f:
        txt = f.read()
        # TODO: triggers a bug!!
        assert pytoml.loads(txt) == expected

def test_string_special():
    expected = {
        'null': '\0',
        'tab': '\t',
        'newline': '\n',
        'cr': '\r',
        'singlequote1': "'",
        'singlequote2': "'",
        'doublequote1': '"',
        'doublequote2': '"',
        'backslash': '\\',
    }
    with open(os.path.join(TOMLS, 'string', 'string-special1.toml')) as f:
        txt = f.read()
        # TODO: triggers a bug!!
        assert pytoml.loads(txt) == expected

@raises(ParseException)
def test_string_invalid1():
    with open(os.path.join(TOMLS, 'string', 'invalid-string1.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_string_invalid2():
    with open(os.path.join(TOMLS, 'string', 'invalid-string2.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_string_invalid3():
    with open(os.path.join(TOMLS, 'string', 'invalid-string3.toml')) as f:
        pytoml.loads(f.read())


# Variable names
def test_var_basic():
    expected = {'ip': '1.1.1.1', 'IP': '4.4.4.4'}
    with open(os.path.join(TOMLS, 'vars', 'var-basic1.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

@raises(ParseException)
def test_var_invalid1():
    with open(os.path.join(TOMLS, 'vars', 'invalid-var1.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_var_invalid2():
    with open(os.path.join(TOMLS, 'vars', 'invalid-var2.toml')) as f:
        pytoml.loads(f.read())


# Arrays
def test_array_basic():
    expected = {'ports': [8001, 8001, 8002]}
    with open(os.path.join(TOMLS, 'array', 'array-basic.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

def test_array_multiline():
    expected = {'key': [1, 2, 3]}
    with open(os.path.join(TOMLS, 'array', 'array-multiline.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

def test_array_nested():
    expected = {'twoarrays': [[1, 2], ['a', 'b', 'c']]}
    with open(os.path.join(TOMLS, 'array', 'array-nested.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

def test_array_trailing():
    expected = {'t': [1, 2, 3, 5, 7]}
    with open(os.path.join(TOMLS, 'array', 'array-trailing.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected

@raises(ParseException)
def test_array_invalid1():
    with open(os.path.join(TOMLS, 'array', 'array-invalid1.toml')) as f:
        pytoml.loads(f.read())


# Hashes
def test_hash_basic1():
    expected = {'owner': {'name': 'David Fischer'}}
    with open(os.path.join(TOMLS, 'hash', 'hash-basic1.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected
    
def test_hash_basic2():
    expected = {'key': {'tater': {'type': 'pug'}}}
    with open(os.path.join(TOMLS, 'hash', 'hash-basic2.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected
    
def test_hash_empty():
    expected = {'empty': {}}
    with open(os.path.join(TOMLS, 'hash', 'hash-empty.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected
    
@raises(NameError)
def test_hash_invalid1():
    with open(os.path.join(TOMLS, 'hash', 'invalid-hash1.toml')) as f:
        pytoml.loads(f.read())

@raises(ParseException)
def test_hash_invalid2():
    with open(os.path.join(TOMLS, 'hash', 'invalid-hash2.toml')) as f:
        pytoml.loads(f.read())


# Complete tests
def test_complete1():
    expected = {
        'title': "TOML Example",
        'owner': {
            'name': "Tom Preston-Werner",
            'organization': "GitHub",
            'bio': "GitHub Cofounder & CEO\nLikes tater tots and beer.",
            'dob': dt.strptime("1979-05-27T07:32:00Z",
                              pytoml.TOMLParser.ISO8601),
        },
        'database': {
            'server': "192.168.1.1",
            'ports': [8001, 8001, 8002],
            'connection_max': 5000,
            'enabled': True,
        },
        'servers': {
            'alpha': {'ip': "10.0.0.1", 'dc': "eqdc10"},
            'beta': {'ip': "10.0.0.2", 'dc': "eqdc10"}
        },
        'clients': {'data': [["gamma", "delta"], [1, 2]]},
    }
    with open(os.path.join(TOMLS, 'complete', 'complete1.toml')) as f:
        txt = f.read()
        assert pytoml.loads(txt) == expected
