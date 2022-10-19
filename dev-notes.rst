Dealing with Agents not supported by httpagentparser
====================================================

.. code:: python

    import httpagentparser as hap

    class JakartaHTTPClinet(hap.Browser):
        name = 'Jakarta Commons-HttpClient'
        look_for = name
        version_splitters = ["/"]

    class SomeNotSoCommonClient(hap.Browser):
        name = 'NotSoCommon Client'
        look_for = 'NotSoCommon'
        def getVersion(self, agent):
            return agent.split(':')[1]

    # Registering new UAs

    hap.detectorshub.register(JakartaHTTPClinet())
    hap.detectorshub.register(SomeNotSoCommonClient())

    # Tests

    s = "Jakarta Commons-HttpClient/3.1"

    print(hap.detect(s))
    print(hap.simple_detect(s))

    s = "NotSoCommon:3.1"

    print(hap.detect(s))
    print(hap.simple_detect(s))

Build and upload new version
============================

- Bump __version__ in httpagentparser/__init__.py
- python setup.py sdist upload

Test httpagentparser
====================

- python tests.py
  
Tox
---

To test httpagentparser from some Python versions, execute the command below (`tox <https://pypi.python.org/pypi/tox>`_ is required).

- python setup.py test
- (or python -m tox)
