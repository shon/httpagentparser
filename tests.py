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
    {'bot': False, 'flavor': {'version': 'X 10.5', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '3.0.10', 'name': 'Firefox', 'family': 'Firefox'}},),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24,gzip(gfe)",
    ('MacOS Macintosh X 10.6.6', 'Chrome 11.0.696.3'),
    {'bot': False, 'flavor': {'version': 'X 10.6.6', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '11.0.696.3', 'name': 'Chrome', 'family': 'Chrome'}},),
("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
    ('Ubuntu Linux 10.04', 'Firefox 3.6'),
    {'bot': False, 'dist': {'version': '10.04', 'name': 'Ubuntu'}, 'os': {'name': 'Linux'}, 'browser': {'version': '3.6', 'name': 'Firefox', 'family': 'Firefox'}},),
("Mozilla/5.0 (Linux; U; Android 2.2.1; fr-ch; A43 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    ('Android Linux 2.2.1', 'AndroidBrowser'),
    {'bot': False, 'dist': {'version': '2.2.1', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'name': 'AndroidBrowser', 'family':'AndroidBrowser'}},),
("Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
    ('iPhone iOS', 'Safari 3.0'),
    {'bot': False, 'os': {'name': 'iOS'}, 'dist': {'name': 'iPhone'}, 'browser': {'version': '3.0', 'name': 'Safari', 'family': 'Safari'}},),
("Mozilla/5.0 (X11; CrOS i686 0.0.0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.27 Safari/534.24,gzip(gfe)",
    ('ChromeOS 0.0.0', 'Chrome 11.0.696.27'),
    {'bot': False, 'os': {'name': 'ChromeOS', 'version': '0.0.0'}, 'browser': {'name': 'Chrome', 'version': '11.0.696.27', 'family': 'Chrome'}},),
("Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]",
    ('Windows XP', 'Opera 7.02'),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Opera', 'version': '7.02', 'family': 'Opera'}},),
("Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    ('Windows 7', 'Microsoft Internet Explorer 10.0'),
    {'bot': False, 'os': {'version': '7', 'name': 'Windows'}, 'browser': {'version': '10.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)",
    ('Windows 7', 'Microsoft Internet Explorer 9.0'),
    {'bot': False, 'os': {'version': '7', 'name': 'Windows'}, 'browser': {'version': '9.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648",
    ('Macintosh', 'Microsoft Internet Explorer 7.0'),
    {'bot': False, 'os': {'name': 'Macintosh'}, 'browser': {'version': '7.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}}),
("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB6.5; QQDownload 534; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
    ('Windows XP', 'Microsoft Internet Explorer 8.0'),
    {'bot': False, 'os': {'version': 'XP', 'name': 'Windows'}, 'browser': {'version': '8.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}}),
('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET4.0C)',
    ('Windows XP', 'Microsoft Internet Explorer 8.0'),
    {'bot': False, 'os': {'version': 'XP', 'name': 'Windows'}, 'browser': {'version': '8.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}},),
("Opera/9.80 (X11; Linux i686; U; en) Presto/2.9.168 Version/11.50",
    ("Linux", "Opera 11.50"),
 {'bot': False, "os": {"name": "Linux"}, "browser": {"name": "Opera", "version": "11.50", 'family': 'Opera'}},),
("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1",
    ("Windows XP", "Netscape 8.1"),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Netscape', 'version': '8.1', 'family': 'Netscape'}},),
("Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    ("WebOS Linux 3.0.2", "WOSBrowser"),
    {'bot': False, 'dist': {'name': 'WebOS', 'version': '3.0.2'}, 'os' : {'name' : 'Linux'}, 'browser': {'name': 'WOSBrowser', 'family': 'WOSBrowser'}},),
("Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3",
    ('IPad iOS 5.0.1', 'Safari 5.1'),
    {'bot': False, 'os': {'name': 'iOS'}, 'dist': {'version': '5.0.1', 'name': 'IPad'}, 'browser': {'version': '5.1', 'name': 'Safari', 'family': 'Safari'}},),
("Mozilla/5.0 (Linux; U; Android 3.2.1; en-gb; Transformer TF101 Build/HTK75) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    ('Android Linux 3.2.1', 'AndroidBrowser'),
    {'bot': False, 'dist': {'version': '3.2.1', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'name': 'AndroidBrowser', 'family': 'AndroidBrowser'}},),
("Mozilla/5.0 (BlackBerry; U; BlackBerry 9700; en-US) AppleWebKit/534.8+ (KHTML, like Gecko) Version/6.0.0.448 Mobile Safari/534.8+",
    ('Blackberry', 'Safari 6.0.0.448'),
    {'bot': False, 'os': {'name': 'Blackberry'}, 'browser': {'version': '6.0.0.448', 'name': 'Safari', 'family': 'Safari'}},),
("Mozilla/5.0 (PlayBook; U; RIM Tablet OS 1.0.0; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.7 Safari/534.11+",
    ('BlackberryPlaybook', 'Safari 7.1.0.7'),
    {'bot': False, 'dist': {'name': 'BlackberryPlaybook'}, 'browser': {'version': '7.1.0.7', 'name': 'Safari', 'family': 'Safari'}},),
("Opera/9.80 (Android 2.3.5; Linux; Opera Mobi/build-1203300859; U; en) Presto/2.10.254 Version/12.00",
    ('Android Linux 2.3.5', 'Opera Mobile 12.00'),
    {'bot': False, 'dist': {'version': '2.3.5', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'version': '12.00', 'name': 'Opera Mobile', 'family': 'Opera'}},),
("Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; HTC_DesireS_S510e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    ('Android Linux 2.3.5', 'AndroidBrowser'),
    {'bot': False, 'dist': {'version': '2.3.5', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'name': 'AndroidBrowser', 'family': 'AndroidBrowser'}},),
("Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; es-es) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3",
    ('iPhone iOS 5.1.1', 'ChromeiOS 19.0.1084.60'),
    {'bot': False, 'os': {'name': 'iOS'}, 'dist': {'version': '5.1.1', 'name': 'iPhone'}, 'browser': {'version': '19.0.1084.60', 'name': 'ChromeiOS', 'family': 'Chrome'}}),
("Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20111011 Firefox/7.0.1 SeaMonkey/2.4.1",
    ("Linux", "SeaMonkey 2.4.1"),
    {'bot': False, "os" : {"name": "Linux"}, "browser": {"name": "SeaMonkey", "version": "2.4.1", 'family': 'SeaMonkey'}}),
("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    ("Ubuntu Linux", "Firefox 16.0"),
    {'bot': False, 'dist': {'name': 'Ubuntu'}, 'os': {'name': 'Linux'}, 'browser': {'version': '16.0', 'name': 'Firefox', 'family': 'Firefox'}},),
("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.1 Safari/537.17",
    ("Linux", "Chrome 24.0.1312.1"),
    {'bot': False, "os" : {"name": "Linux"}, "browser": {"name": "Chrome", "version": "24.0.1312.1", 'family': 'Chrome'}}),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.19 (KHTML, like Gecko) Chrome/25.0.1323.1 Safari/537.19",
    ("MacOS Macintosh X 10.8.2", "Chrome 25.0.1323.1"),
    {'bot': False, 'flavor': {'name': 'MacOS', 'version': 'X 10.8.2'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '25.0.1323.1', 'name': 'Chrome', 'family': 'Chrome'}},),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14",
    ("MacOS Macintosh X 10.8.2", "Safari 6.0.1"),
    {'bot': False, 'flavor': {'name': 'MacOS', 'version': 'X 10.8.2'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '6.0.1', 'name': 'Safari', 'family': 'Safari'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    ("Windows 7", "Chrome 23.0.1271.64"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '23.0.1271.64', 'name': 'Chrome', 'family': 'Chrome'}},),
("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
    ("Windows XP", "Microsoft Internet Explorer 8.0"),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'version': '8.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    ("Windows 7", "Microsoft Internet Explorer 9.0"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '9.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    ("Windows 7", "Firefox 15.0.1"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '15.0.1', 'name': 'Firefox', 'family': 'Firefox'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    ("Windows 7", "Safari 5.1.7"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '5.1.7', 'name': 'Safari', 'family': 'Safari'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36 OPR/17.0.1241.53",
    ("Windows 7", "Opera 17.0.1241.53"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '17.0.1241.53', 'name': 'Opera', 'family': 'Opera'}},),
('Mozilla/5.0+(X11;+CrOS+i686+2465.163.0)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.91+Safari/537.1',
    ('ChromeOS 2465.163.0', 'Chrome 21.0.1180.91'),
    {'bot': False, 'os': {'version': '2465.163.0', 'name': 'ChromeOS'}, 'browser': {'version': '21.0.1180.91', 'name': 'Chrome', 'family': 'Chrome'}},),
('Mozilla/5.0 (Linux; U; en-us; KFOT Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Silk/2.2 Safari/535.19 Silk-Accelerated=true',
    ('Linux', 'Safari 535.19'),
    {'bot': False, 'os': {'name': 'Linux'}, 'browser': {'version': '535.19', 'name': 'Safari', 'family': 'Safari'}}),
('Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    ('Windows 8.1', 'Microsoft Internet Explorer 11.0'),
    {'bot': False, 'os': {'name': 'Windows', 'version': '8.1'}, 'browser': {'version': '11.0', 'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer'}},),
('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    ('Unknown OS', 'GoogleBot 2.1'),
    {'bot': True, 'browser': {'name': 'GoogleBot', 'version': '2.1', 'family': 'GoogleBot'}},),
('"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"',
    ('Unknown OS', 'BingBot 2.0'),
 {'bot': True, 'browser': {'name': 'BingBot', 'version': '2.0', 'family': 'BingBot'}}),
('Mozilla/5.0 (compatible; YandexBot/3.0)',
    ('Unknown OS', 'YandexBot 3.0'),
    {'bot': True, 'browser': {'name': 'YandexBot', 'version': '3.0', 'family': 'YandexBot'}}),
('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    ('Unknown OS', 'BaiduBot 2.0'),
    {'bot': True, 'browser': {'name': 'BaiduBot', 'version': '2.0', 'family': 'BaiduBot'}}),
('Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Radar 4G)',
    ('Windows Phone 7.5', 'Microsoft Internet Explorer 9.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer', 'version': '9.0'}, 'os': {'name': 'Windows Phone', 'version': '7.5'}}),
('Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; SAMSUNG; GT-i8700)',
    ('Windows Phone 7.0', 'Microsoft Internet Explorer 7.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer', 'version': '7.0'}, 'os': {'name': 'Windows Phone', 'version': '7.0'}}),
('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; HTC_HD2_T8585; Windows Phone 6.5)',
    ('Windows Phone 6.5', 'Microsoft Internet Explorer 6.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'family': 'Microsoft Internet Explorer', 'version': '6.0'}, 'os': {'name': 'Windows Phone', 'version': '6.5'}}),
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
            detected = detect(agent)
            del detected['platform']
            self.assertEqual(detected, res)

    def test_bot(self):
        s = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        d = detect(s)
        self.assertTrue(d['bot'])

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

    def test_fill_none(self):
        self.assertEqual(detect(''), {'platform': {'version': None, 'name': None}})  # default
        self.assertEqual(detect('', fill_none=False), {'platform': {'version': None, 'name': None}})
        result = detect('', fill_none=True)
        self.assertEqual(result['os'].get('name'), None)
        self.assertEqual(result['browser'].get('version'), None)

if __name__ == '__main__':
    unittest.main()
