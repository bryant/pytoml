from pyparsing import (
    Combine, Optional, Regex, Forward, Group, Suppress, Keyword, LineEnd, Or,
    ZeroOrMore, QuotedString, nums, Word, pythonStyleComment, printables,
    ParseException,
)
from datetime import datetime
import re
import sys

PY3 = sys.version_info[0] == 3

if PY3:
    def unescape(s):
        return bytes(s, "utf-8").decode("unicode_escape")
else:
    def unescape(s):
        return s.decode("string_escape")

ISO8601 = "%Y-%m-%dT%H:%M:%SZ"


class TOMLParser(object):
    # Grammar.
    basic_int = Optional("-") + ("0" | Word(nums))

    string = QuotedString("\"", escChar="\\")
    integer = Combine(basic_int)
    float_ = Combine(basic_int + "." + Word(nums))
    datetime = Regex(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
    boolean = Keyword("true") | Keyword("false")

    array = Forward()
    array_delim = comma = Suppress(",")

    string_array = string + ZeroOrMore(comma + string) + Optional(comma)
    integer_array = integer + ZeroOrMore(comma + integer) + Optional(comma)
    float_array = float_ + ZeroOrMore(comma + float_) + Optional(comma)
    datetime_array = datetime + ZeroOrMore(comma + datetime) + Optional(comma)
    boolean_array = boolean + ZeroOrMore(comma + boolean) + Optional(comma)
    array_array = array + ZeroOrMore(comma + array) + Optional(comma)

    array <<  Group(Suppress("[")
                    + (datetime_array | string_array | integer_array |
                       float_array | boolean_array)
                    + Suppress("]"))

    key_name = Word(re.sub(r"[\[\]=\"]", "", printables))
    value = datetime | string | integer | float_ | boolean | array
    keyvalue = key_name + "=" + value + LineEnd()

    kgrp_name = Word(re.sub(r"[\[\]\.]", "", printables))
    keygroup_namespace = kgrp_name + ZeroOrMore(Suppress(".") + kgrp_name)
    keygroup = Suppress("[") + keygroup_namespace + Suppress("]") + LineEnd()

    comments = pythonStyleComment

    toml_doc = ZeroOrMore(keyvalue | keygroup).ignore(comments)


    def _parse_string(self, src, loc, toks):
        # only permit toml-reserved escapes.
        match = re.search(r"(?<!\\)(\\[^0tnr\"\\])", toks[0])
        if match:
            raise ParseException("Reserved escape sequence \"%s\"" %
                                 match.group(), loc)
        return unescape(toks[0])

    def _parse_integer(self, src, loc, toks):
        return int(toks[0])

    def _parse_float_(self, src, loc, toks):
        return float(toks[0])

    def _parse_boolean(self, src, loc, toks):
        return bool(toks[0])

    def _parse_datetime(self, src, loc, toks):
        try:
            return datetime.strptime(toks[0], ISO8601)
        except ValueError:
            # this informative error message will never make it out because
            # pyparsing catches ParseBaseException and reraises on its own.
            # oh well.
            raise ParseException("invalid datetime \"%s\"" % toks[0], loc)

    def _parse_array(self, src, loc, toks):
        return [toks[0]]

    def _parse_keyvalue(self, src, loc, toks):
        k, v = toks.asList()
        if k in self._cur:
            raise ParseException("key %s already exists" % k, loc)
        self._cur[k] = v

    def _parse_keygroup_namespace(self, src, loc, toks):
        cur = self._root
        for subname in toks:
            subspace = cur.get(subname, {})
            if not isinstance(subspace, dict):
                raise ParseException("key %s already exists" % subname, loc)
            cur = cur.setdefault(subname, subspace)
        self._cur = cur

    for entity in ("string", "integer", "float_", "datetime", "boolean",
                   "array", "keyvalue", "keygroup_namespace"):
        locals()[entity].setParseAction(locals()["_parse_"+entity])

    def parse(self, s):
        self._root = {}
        self._cur = self._root
        self.toml_doc.parseWithTabs()
        self.toml_doc.parseString(s, parseAll=True)
        return self._root

def loads(string):
    return TOMLParser().parse(string)

if __name__ == "__main__":
    from sys import stdin
    from pprint import pprint
    pprint(loads(stdin.read()))
