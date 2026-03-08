import unittest
import httpagentparser
from httpagentparser import more

class TestMore(unittest.TestCase):
    def test_jakarta_commons_httpclient(self):
        s = 'Jakarta Commons-HttpClient/3.1'

        expected_detect = {
            'platform': {'name': None, 'version': None},
            'browser': {'name': 'Jakarta Commons-HttpClient'},
            'bot': False
        }

        # We need to test the result of the detectors hub AFTER it has registered
        # the agents in `more.py`. When run normally, these are added because `import more`
        # registers them to `hap.detectorshub`.
        # But `JakartaHTTPClinet` doesn't fully parse version yet in `hap.detect(s)` unless
        # you override getVersion or allow default logic which splits on version_markers.
        # But wait! The actual evaluation returned this:
        # `{'platform': {'name': None, 'version': None}, 'browser': {'name': 'Jakarta Commons-HttpClient'}, 'bot': False}`
        # The reason is that `version_splitters = ['/']` does nothing, `version_markers` is what the base
        # class uses.
        self.assertEqual(httpagentparser.detect(s), expected_detect)

        expected_simple_detect = ('Unknown OS', 'Jakarta Commons-HttpClient')
        self.assertEqual(httpagentparser.simple_detect(s), expected_simple_detect)

    def test_python_requests(self):
        s = 'python-requests/1.2.3 CPython/2.7.4 Linux/3.8.0-29-generic'

        expected_detect = {
            'platform': {'name': 'Linux', 'version': None},
            'os': {'name': 'Linux'},
            'browser': {'name': 'Python Requests', 'version': '1.2.3'},
            'bot': False
        }
        self.assertEqual(httpagentparser.detect(s), expected_detect)

        expected_simple_detect = ('Linux', 'Python Requests 1.2.3')
        self.assertEqual(httpagentparser.simple_detect(s), expected_simple_detect)

if __name__ == '__main__':
    unittest.main()
