pytoml
======

A [TOML](https://github.com/mojombo/toml) parser for Python 2/3 which conforms
to
[0726febe811a819f3a25ac71ed7703527c20dc76](https://github.com/mojombo/toml/commit/0726febe811a819f3a25ac71ed7703527c20dc76)
and earlier.

```python
>>> import pytoml
>>> pytoml.loads('hooray = ["for", "toml"]')
{'hooray': [u'for', u'toml']}
```
