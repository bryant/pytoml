from pyparsing import (
    Combine, Optional, Regex, Forward, Group, Suppress, Keyword, LineEnd, Or,
    ZeroOrMore, QuotedString, nums, Word, pythonStyleComment, printables,
)
from datetime import datetime
from re import sub
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    def unescape(s):
        return bytes(s, "utf-8").decode("unicode_escape")
else:
    def unescape(s):
        return s.decode("unicode_escape")

def delimitedList(type_, delimiter=","):
    return (type_ + ZeroOrMore(Suppress(delimiter) + type_) +
            Optional(Suppress(delimiter)))

class TOMLParser(object):
    def __init__(self):
        key_name = Word(sub(r"[\[\]=\"]", "", printables))
        kgrp_name = Word(sub(r"[\[\]\.]", "", printables))
        basic_int = Optional("-") + ("0" | Word(nums))

        types = dict(
            string = QuotedString("\""),
            integer = Combine(basic_int),
            float = Combine(basic_int + "." + Word(nums)),
            datetime = Regex(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"),
            boolean = Keyword("true") | Keyword("false"),
            array = Forward(),
        )

        pure_array = Or(delimitedList(type_) for type_ in types.values())
        types["array"] << Group(Suppress("[") + Optional(pure_array) +
                                Suppress("]"))

        value = Or(type_ for type_ in types.values())
        keyvalue = key_name + Suppress("=") + value + Suppress(LineEnd())
        keygroup_namespace = kgrp_name + ZeroOrMore(Suppress(".") + kgrp_name)
        keygroup = "[" + keygroup_namespace + "]" + LineEnd()
        comments = pythonStyleComment

        self._toplevel = ZeroOrMore(keyvalue | keygroup)
        self._toplevel.ignore(comments)

        for k, v in types.items():
            v.setParseAction(getattr(self, "_parse_"+k))
        keyvalue.setParseAction(self._parse_keyvalue)
        keygroup_namespace.setParseAction(self._parse_keygroup_namespace)

    _parse_string = lambda self, tok: unescape(tok[0])
    _parse_integer = lambda self, tok: int(tok[0])
    _parse_float = lambda self, tok: float(tok[0])
    _parse_boolean = lambda self, tok: bool(tok[0])

    ISO8601 = "%Y-%m-%dT%H:%M:%SZ"
    _parse_datetime = lambda self, tok: datetime.strptime(tok[0], self.ISO8601)

    _parse_array = lambda self, tok: [tok[0]]

    def _parse_keyvalue(self, s, loc, toks):
        k, v = toks.asList()
        if k in self._cur:
            raise NameError("key %s already exists" % k)
        self._cur[k] = v

    def _parse_keygroup_namespace(self, s, loc, toks):
        cur = self._root
        for subname in toks:
            subspace = cur.get(subname, {})
            if not isinstance(subspace, dict):
                raise NameError("key %s already exists" % subname)
            cur = cur.setdefault(subname, subspace)
        self._cur = cur

    def parse(self, s):
        self._root = {}
        self._cur = self._root
        self._toplevel.parseWithTabs()
        self._toplevel.parseString(s, parseAll=True)
        return self._root

def loads(string):
    return TOMLParser().parse(string)

if __name__ == "__main__":
    from sys import stdin
    from pprint import pprint
    pprint(loads(stdin.read()))
