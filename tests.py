from datetime import datetime as dt
from nose.tools import raises
from pyparsing import ParseException
import pytoml

def test_basic():
    source = """\
# This is a TOML document. Boom.

title = "TOML Example"

[owner]
name = "Tom Preston-Werner"
organization = "GitHub"
bio = "GitHub Cofounder & CEO\\nLikes tater tots and beer."
dob = 1979-05-27T07:32:00Z # First class dates? Why not?

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

  # You can indent as you please. Tabs or spaces. TOML don't care.
  [servers.alpha]
  ip = "10.0.0.1"
  dc = "eqdc10"

  [servers.beta]
  ip = "10.0.0.2"
  dc = "eqdc10"

[clients]
data = [ ["gamma", "delta"], [1, 2] ] # just an update to make sure parsers support it
"""
    expected = dict(
        title = "TOML Example",
        owner = dict(
            name = "Tom Preston-Werner",
            organization = "GitHub",
            bio = "GitHub Cofounder & CEO\nLikes tater tots and beer.",
            dob = dt.strptime("1979-05-27T07:32:00Z",
                              pytoml.TOMLParser.ISO8601),
        ),
        database = dict(
            server = "192.168.1.1",
            ports = [8001, 8001, 8002],
            connection_max = 5000,
            enabled = True,
        ),
        servers = dict(
            alpha = dict(ip = "10.0.0.1", dc = "eqdc10"),
            beta = dict(ip = "10.0.0.2", dc = "eqdc10")
        ),
        clients = dict(data = [["gamma", "delta"], [1, 2]]),
    )

    assert pytoml.loads(source) == expected

@raises(NameError)
def test_no_overwrite():
    source = """\
storks = "evil"
[storks]
should = ["never", "reach", "here"]
"""
    pytoml.loads(source)

@raises(ParseException)
def test_pure_array():
    source = "impure_list = [1, 2, 3, \"fail\"]"
    pytoml.loads(source)

def test_terminating_comma():
    source = """\
# toml
key = [
    1,
    2,  # this is okay
]
"""
    expected = {"key": [1, 2]}
    assert pytoml.loads(source) == expected
