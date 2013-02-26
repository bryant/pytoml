pytoml
======

A [TOML](https://github.com/mojombo/toml) parser for Python 2/3 which conforms
to [0726febe](https://github.com/mojombo/toml/commit/0726febe) and earlier.

```python
>>> import pytoml
>>> pytoml.loads('hooray = ["for", "toml"]')
{'hooray': [u'for', u'toml']}
```


Features
--------

* Uses [pyparsing](http://pyparsing.wikispaces.com/) and a formal grammar
* Extensive test suite and sample files

