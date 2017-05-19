|Number of PyPI downloads|

Features
--------

- Works on Python 2.7 and Python 3
- Fast
- Detects OS and Browser. Does not aim to be a full featured agent parser
- Will not turn into django-httpagentparser ;)

Usage
-----

.. code-block:: python

    >>> import httpagentparser
    >>> s = "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) \
            Chrome/5.0.307.11 Safari/532.9"
    >>> print httpagentparser.simple_detect(s)
    ('Linux', 'Chrome 5.0.307.11')
    >>> print httpagentparser.detect(s)
    {'os': {'name': 'Linux'},
     'browser': {'version': '5.0.307.11', 'name': 'Chrome'}}

    >>> s = "Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; HTC_DesireS_S510e Build/GRJ90) \
            AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
    >>> print httpagentparser.simple_detect(s)
    ('Android Linux 2.3.5', 'Safari 4.0')
    >>> print httpagentparser.detect(s)
    {'dist': {'version': '2.3.5', 'name': 'Android'},
    'os': {'name': 'Linux'},
    'browser': {'version': '4.0', 'name': 'Safari'}}

History
-------

http://stackoverflow.com/questions/927552/parsing-http-user-agent-string/1151956#1151956


.. |Number of PyPI downloads| image:: https://pypip.in/d/httpagentparser.png
   :target: https://crate.io/packages/httpagentparser/
