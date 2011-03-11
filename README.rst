Usage
-----

::

    >>> import httpagentparser
    >>> s = "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.307.11 Safari/532.9"
    >>> print httpagentparser.simple_detect(s)
    ('Linux', 'Chrome 5.0.307.11')
    >>> print httpagentparser.detect(s)
    {'os': {'name': 'Linux'},
     'browser': {'version': '5.0.307.11', 'name': 'Chrome'}}

