import unittest
import time
import httpagentparser

detect = httpagentparser.detect
simple_detect = httpagentparser.simple_detect

data = (
# tuple of tuples
# tuple (agent-string, expected result of simple_detect, expected result of detect)
    ("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10",
    ('MacOS Macintosh X 10.5', 'Firefox 3.0.10'),
    {'flavor': {'version': 'X 10.5', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '3.0.10', 'name': 'Firefox'}},),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24,gzip(gfe)",
    ('MacOS Macintosh X 10.6.6', 'Chrome 11.0.696.3'),
    {'flavor': {'version': 'X 10.6.6', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '11.0.696.3', 'name': 'Chrome'}},),
("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
    ('Ubuntu Linux 10.04', 'Firefox 3.6'),
    {'dist': {'version': '10.04', 'name': 'Ubuntu'}, 'os': {'name': 'Linux'}, 'browser': {'version': '3.6', 'name': 'Firefox'}},),
("Mozilla/5.0 (Linux; U; Android 2.2.1; fr-ch; A43 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    ('Android Linux 2.2.1', 'Safari 4.0'),
    {'dist': {'version': '2.2.1', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'version': '4.0', 'name': 'Safari'}},),
("Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
    ('MacOS IPhone X', 'Safari 3.0'),
    {'flavor': {'version': 'X', 'name': 'MacOS'}, 'dist': {'version': 'X', 'name': 'IPhone'}, 'browser': {'version': '3.0', 'name': 'Safari'}},),
("Mozilla/5.0 (X11; CrOS i686 0.0.0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.27 Safari/534.24,gzip(gfe)",
    ('ChromeOS 0.0.0', 'Chrome 11.0.696.27'),
    {'os': {'name': 'ChromeOS', 'version': '0.0.0'}, 'browser': {'name': 'Chrome', 'version': '11.0.696.27'}},),
("Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]",
    ('Windows XP', 'Opera 7.02'),
    {'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Opera', 'version': '7.02'}},),
("Opera/9.80 (X11; Linux i686; U; en) Presto/2.9.168 Version/11.50",
    ("Linux", "Opera 11.50"),
    {"os": {"name": "Linux"}, "browser": {"name": "Opera", "version": "11.50"}},),
("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1",
    ("Windows XP", "Netscape 8.1"),
    {'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Netscape', 'version': '8.1'}},),
("Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    ("WebOS Linux 3.0.2", "WOSBrowser"),
    {'dist': {'name': 'WebOS', 'version': '3.0.2'}, 'os' : {'name' : 'Linux'}, 'browser': {'name': 'WOSBrowser'}},),
("Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3",
    ('MacOS IPad X', 'Safari 5.1'),
    {'flavor': {'version': 'X', 'name': 'MacOS'}, 'dist': {'version': 'X', 'name': 'IPad'}, 'browser': {'version': '5.1', 'name': 'Safari'}},),
("Mozilla/5.0 (Linux; U; Android 3.2.1; en-gb; Transformer TF101 Build/HTK75) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    ('Android Linux 3.2.1', 'Safari 4.0'),
    {'dist': {'version': '3.2.1', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'version': '4.0', 'name': 'Safari'}},),
("Mozilla/5.0 (BlackBerry; U; BlackBerry 9700; en-US) AppleWebKit/534.8+ (KHTML, like Gecko) Version/6.0.0.448 Mobile Safari/534.8+",
    ('Blackberry', 'Safari 6.0.0.448'),
    {'os': {'name': 'Blackberry'}, 'browser': {'version': '6.0.0.448', 'name': 'Safari'}},),
("Mozilla/5.0 (PlayBook; U; RIM Tablet OS 1.0.0; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.7 Safari/534.11+",
    ('BlackberryPlaybook', 'Safari 7.1.0.7'),
    {'dist': {'name': 'BlackberryPlaybook'}, 'browser': {'version': '7.1.0.7', 'name': 'Safari'}},),
("Opera/9.80 (Android 2.3.5; Linux; Opera Mobi/build-1203300859; U; en) Presto/2.10.254 Version/12.00",
    ('Android Linux 2.3.5', 'Opera Mobile 12.00'),
    {'dist': {'version': '2.3.5', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'version': '12.00', 'name': 'Opera Mobile'}},),
("Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; HTC_DesireS_S510e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    ('Android Linux 2.3.5', 'Safari 4.0'),
    {'dist': {'version': '2.3.5', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'version': '4.0', 'name': 'Safari'}},),
    ("Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; es-es) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3",
    ('MacOS IPhone X', 'ChromeiOS 19.0.1084.60'),
    {'flavor': {'version': 'X', 'name': 'MacOS'}, 'dist': {'version': 'X', 'name': 'IPhone'}, 'browser': {'version': '19.0.1084.60', 'name': 'ChromeiOS'}},),
)

class TestHAP(unittest.TestCase):
    def setUp(self):
        self.harass_repeat = 1000
        self.data = data

    def test_simple_detect(self):
        for agent, simple_res, res in data:
            self.assertEqual(simple_detect(agent), simple_res)

    def test_detect(self):
        for agent, simple_res, res in data:
            self.assertEqual(detect(agent), res)

    def test_harass(self):
        then = time.time()
        for agent, simple_res, res in data * self.harass_repeat:
            detect(agent)
        time_taken = time.time() - then
        no_of_tests = len(self.data) * self.harass_repeat
        print("\nTime taken for %s detections: %s" %
            (no_of_tests, time_taken))
        print("Time taken for single detection: %f" %
            (time_taken / (len(self.data) * self.harass_repeat)))

if __name__ == '__main__':
    unittest.main()
