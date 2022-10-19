import unittest
import time
import httpagentparser

detect = httpagentparser.detect
simple_detect = httpagentparser.simple_detect

data = (
# tuple of tuples
# tuple (agent-string, expected result of simple_detect, expected result of detect)
("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3861.0 Safari/537.36 Edg/77.0.230.2",
    ('Windows 10', 'ChromiumEdge 77.0.230.2'),
    {'bot': False, 'os': {'version': '10', 'name': 'Windows'},  'browser': {'version': '77.0.230.2', 'name': 'ChromiumEdge'}},),
("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10",
    ('MacOS Macintosh X 10.5', 'Firefox 3.0.10'),
    {'bot': False, 'flavor': {'version': 'X 10.5', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '3.0.10', 'name': 'Firefox'}},),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24,gzip(gfe)",
    ('MacOS Macintosh X 10.6.6', 'Chrome 11.0.696.3'),
    {'bot': False, 'flavor': {'version': 'X 10.6.6', 'name': 'MacOS'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '11.0.696.3', 'name': 'Chrome'}},),
("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
    ('Ubuntu Linux 10.04', 'Firefox 3.6'),
    {'bot': False, 'dist': {'version': '10.04', 'name': 'Ubuntu'}, 'os': {'name': 'Linux'}, 'browser': {'version': '3.6', 'name': 'Firefox'}},),
("Mozilla/5.0 (Linux; U; Android 2.2.1; fr-ch; A43 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    ('Android Linux 2.2.1', 'AndroidBrowser'),
    {'bot': False, 'dist': {'version': '2.2.1', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'name': 'AndroidBrowser'}},),
("Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3",
    ('iPhone iOS', 'Safari 3.0'),
    {'bot': False, 'os': {'name': 'iOS'}, 'dist': {'name': 'iPhone'}, 'browser': {'version': '3.0', 'name': 'Safari'}},),
("Mozilla/5.0 (X11; CrOS i686 0.0.0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.27 Safari/534.24,gzip(gfe)",
    ('ChromeOS 0.0.0', 'Chrome 11.0.696.27'),
    {'bot': False, 'os': {'name': 'ChromeOS', 'version': '0.0.0'}, 'browser': {'name': 'Chrome', 'version': '11.0.696.27'}},),
("Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.1) Opera 7.02 [en]",
    ('Windows XP', 'Opera 7.02'),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Opera', 'version': '7.02'}},),
("Opera/9.64(Windows NT 5.1; U; en) Presto/2.1.1",
    ('Windows XP', 'Opera 9.64'),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Opera', 'version': '9.64'}},),
("Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    ('Windows 7', 'Microsoft Internet Explorer 10.0'),
    {'bot': False, 'os': {'version': '7', 'name': 'Windows'}, 'browser': {'version': '10.0', 'name': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)",
    ('Windows 7', 'Microsoft Internet Explorer 9.0'),
    {'bot': False, 'os': {'version': '7', 'name': 'Windows'}, 'browser': {'version': '9.0', 'name': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648",
    ('Macintosh', 'Microsoft Internet Explorer 7.0'),
    {'bot': False, 'os': {'name': 'Macintosh'}, 'browser': {'version': '7.0', 'name': 'Microsoft Internet Explorer'}}),
("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB6.5; QQDownload 534; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
    ('Windows XP', 'Microsoft Internet Explorer 8.0'),
    {'bot': False, 'os': {'version': 'XP', 'name': 'Windows'}, 'browser': {'version': '8.0', 'name': 'Microsoft Internet Explorer'}}),
('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; SLCC1; .NET CLR 2.0.50727; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET4.0C)',
    ('Windows XP', 'Microsoft Internet Explorer 8.0'),
    {'bot': False, 'os': {'version': 'XP', 'name': 'Windows'}, 'browser': {'version': '8.0', 'name': 'Microsoft Internet Explorer'}},),
("Opera/9.80 (X11; Linux i686; U; en) Presto/2.9.168 Version/11.50",
    ("Linux", "Opera 11.50"),
 {'bot': False, "os": {"name": "Linux"}, "browser": {"name": "Opera", "version": "11.50"}},),
("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1",
    ("Windows XP", "Netscape 8.1"),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'name': 'Netscape', 'version': '8.1'}},),
("Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0",
    ("WebOS Linux 3.0.2", "WOSBrowser"),
    {'bot': False, 'dist': {'name': 'WebOS', 'version': '3.0.2'}, 'os' : {'name' : 'Linux'}, 'browser': {'name': 'WOSBrowser'}},),
("Mozilla/5.0 (iPad; CPU OS 5_0_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A405 Safari/7534.48.3",
    ('IPad iOS 5.0.1', 'Safari 5.1'),
    {'bot': False, 'os': {'name': 'iOS'}, 'dist': {'version': '5.0.1', 'name': 'IPad'}, 'browser': {'version': '5.1', 'name': 'Safari'}},),
("AppleCoreMedia/1.0.0.10B329 (iPad; U; CPU OS 6_1_3 like Mac OS X; en_us)",
    ('IPad iOS 6.1.3', 'Unknown Browser'),
    {'bot': False, 'dist': {'name': 'IPad', 'version': '6.1.3'}, 'os': {'name': 'iOS'}},),
("Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53",
    ('IPad iOS 7.1', 'Safari 7.0'),
    {'bot': False, 'browser': {'name': 'Safari', 'version': '7.0'}, 'dist': {'name': 'IPad', 'version': '7.1'}, 'os': {'name': 'iOS'}}),
("Mozilla/5.0 (Linux; U; Android 3.2.1; en-gb; Transformer TF101 Build/HTK75) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    ('Android Linux 3.2.1', 'AndroidBrowser'),
    {'bot': False, 'dist': {'version': '3.2.1', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'name': 'AndroidBrowser'}},),
("Mozilla/5.0 (BlackBerry; U; BlackBerry 9700; en-US) AppleWebKit/534.8+ (KHTML, like Gecko) Version/6.0.0.448 Mobile Safari/534.8+",
    ('Blackberry', 'Safari 6.0.0.448'),
    {'bot': False, 'os': {'name': 'Blackberry'}, 'browser': {'version': '6.0.0.448', 'name': 'Safari'}},),
("Mozilla/5.0 (PlayBook; U; RIM Tablet OS 1.0.0; en-US) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.7 Safari/534.11+",
    ('BlackberryPlaybook', 'Safari 7.1.0.7'),
    {'bot': False, 'dist': {'name': 'BlackberryPlaybook'}, 'browser': {'version': '7.1.0.7', 'name': 'Safari'}},),
("Opera/9.80 (Android 2.3.5; Linux; Opera Mobi/build-1203300859; U; en) Presto/2.10.254 Version/12.00",
    ('Android Linux 2.3.5', 'Opera Mobile 12.00'),
    {'bot': False, 'dist': {'version': '2.3.5', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'version': '12.00', 'name': 'Opera Mobile'}},),
("Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; HTC_DesireS_S510e Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    ('Android Linux 2.3.5', 'AndroidBrowser'),
    {'bot': False, 'dist': {'version': '2.3.5', 'name': 'Android'}, 'os': {'name': 'Linux'}, 'browser': {'name': 'AndroidBrowser'}},),
("Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; es-es) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3",
    ('iPhone iOS 5.1.1', 'ChromeiOS 19.0.1084.60'),
    {'bot': False, 'os': {'name': 'iOS'}, 'dist': {'version': '5.1.1', 'name': 'iPhone'}, 'browser': {'version': '19.0.1084.60', 'name': 'ChromeiOS'}}),
("Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20111011 Firefox/7.0.1 SeaMonkey/2.4.1",
    ("Linux", "SeaMonkey 2.4.1"),
    {'bot': False, "os" : {"name": "Linux"}, "browser": {"name": "SeaMonkey", "version": "2.4.1"}}),
("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    ("Ubuntu Linux", "Firefox 16.0"),
    {'bot': False, 'dist': {'name': 'Ubuntu'}, 'os': {'name': 'Linux'}, 'browser': {'version': '16.0', 'name': 'Firefox'}},),
("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.1 Safari/537.17",
    ("Linux", "Chrome 24.0.1312.1"),
    {'bot': False, "os" : {"name": "Linux"}, "browser": {"name": "Chrome", "version": "24.0.1312.1"}}),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.19 (KHTML, like Gecko) Chrome/25.0.1323.1 Safari/537.19",
    ("MacOS Macintosh X 10.8.2", "Chrome 25.0.1323.1"),
    {'bot': False, 'flavor': {'name': 'MacOS', 'version': 'X 10.8.2'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '25.0.1323.1', 'name': 'Chrome'}},),
("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/536.26.14 (KHTML, like Gecko) Version/6.0.1 Safari/536.26.14",
    ("MacOS Macintosh X 10.8.2", "Safari 6.0.1"),
    {'bot': False, 'flavor': {'name': 'MacOS', 'version': 'X 10.8.2'}, 'os': {'name': 'Macintosh'}, 'browser': {'version': '6.0.1', 'name': 'Safari'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    ("Windows 7", "Chrome 23.0.1271.64"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '23.0.1271.64', 'name': 'Chrome'}},),
("Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)",
    ("Windows XP", "Microsoft Internet Explorer 8.0"),
    {'bot': False, 'os': {'name': 'Windows', 'version': 'XP'}, 'browser': {'version': '8.0', 'name': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    ("Windows 7", "Microsoft Internet Explorer 9.0"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '9.0', 'name': 'Microsoft Internet Explorer'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    ("Windows 7", "Firefox 15.0.1"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '15.0.1', 'name': 'Firefox'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    ("Windows 7", "Safari 5.1.7"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '5.1.7', 'name': 'Safari'}},),
("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36 OPR/17.0.1241.53",
    ("Windows 7", "Opera 17.0.1241.53"),
    {'bot': False, 'os': {'name': 'Windows', 'version': '7'}, 'browser': {'version': '17.0.1241.53', 'name': 'Opera'}},),
('Mozilla/5.0+(X11;+CrOS+i686+2465.163.0)+AppleWebKit/537.1+(KHTML,+like+Gecko)+Chrome/21.0.1180.91+Safari/537.1',
    ('ChromeOS 2465.163.0', 'Chrome 21.0.1180.91'),
    {'bot': False, 'os': {'version': '2465.163.0', 'name': 'ChromeOS'}, 'browser': {'version': '21.0.1180.91', 'name': 'Chrome'}},),
('Mozilla/5.0 (Linux; U; en-us; KFOT Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Silk/2.2 Safari/535.19 Silk-Accelerated=true',
    ('Linux', 'Safari 535.19'),
    {'bot': False, 'os': {'name': 'Linux'}, 'browser': {'version': '535.19', 'name': 'Safari'}}),
('Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    ('Windows 8.1', 'Microsoft Internet Explorer 11.0'),
    {'bot': False, 'os': {'name': 'Windows', 'version': '8.1'}, 'browser': {'version': '11.0', 'name': 'Microsoft Internet Explorer'}},),
('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    ('Unknown OS', 'GoogleBot 2.1'),
    {'bot': True, 'browser': {'name': 'GoogleBot', 'version': '2.1'}},),
('"Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"',
    ('Unknown OS', 'BingBot 2.0'),
 {'bot': True, 'browser': {'name': 'BingBot', 'version': '2.0'}}),
('Mozilla/5.0 (compatible; YandexBot/3.0)',
    ('Unknown OS', 'YandexBot 3.0'),
    {'bot': True, 'browser': {'name': 'YandexBot', 'version': '3.0'}}),
('Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    ('Unknown OS', 'BaiduBot 2.0'),
    {'bot': True, 'browser': {'name': 'BaiduBot', 'version': '2.0'}}),
('Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Radar 4G)',
    ('Windows Phone 7.5', 'Microsoft Internet Explorer 9.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'version': '9.0'}, 'os': {'name': 'Windows Phone', 'version': '7.5'}}),
('Mozilla/4.0 (compatible; MSIE 7.0; Windows Phone OS 7.0; Trident/3.1; IEMobile/7.0; SAMSUNG; GT-i8700)',
    ('Windows Phone 7.0', 'Microsoft Internet Explorer 7.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'version': '7.0'}, 'os': {'name': 'Windows Phone', 'version': '7.0'}}),
('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; HTC_HD2_T8585; Windows Phone 6.5)',
    ('Windows Phone 6.5', 'Microsoft Internet Explorer 6.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'version': '6.0'}, 'os': {'name': 'Windows Phone', 'version': '6.5'}}),
('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; HTC_HD2_T8585; Windows Phone 6.5)',
    ('Windows Phone 6.5', 'Microsoft Internet Explorer 6.0'),
    {'bot': False, 'browser': {'name': 'Microsoft Internet Explorer', 'version': '6.0'}, 'os': {'name': 'Windows Phone', 'version': '6.5'}}),
('Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20110814 Firefox/6.0 Google (+https://developers.google.com/+/web/snippet/)',
    ('Windows 7', 'GoogleBot'),
    {'bot': True, 'browser': {'name': 'GoogleBot'}, 'os': {'name': 'Windows', 'version': '7'}}),
('facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    ('Unknown OS', 'FacebookExternalHit 1.1'),
    {'bot': True, 'browser': {'name': 'FacebookExternalHit', 'version': '1.1'},}),
('runscope-radar/2.0',
    ('Unknown OS', 'RunscopeRadar'),
    {'bot': True, 'browser': {'name': 'RunscopeRadar'}}),
('Mozilla/5.0 (Mobile; Windows Phone 8.1; Android 4.0; ARM; Trident/7.0; Touch; rv:11.0; IEMobile/11.0; NOKIA; Lumia 720) like iPhone OS 7_0_3 Mac OS X AppleWebKit/537 (KHTML, like Gecko) Mobile Safari/537',
    ('Windows Phone 8.1', 'Microsoft Internet Explorer 11.0'),
    {'os': {'version': '8.1', 'name': 'Windows Phone'}, 'bot': False, 'browser': {'version': '11.0', 'name': 'Microsoft Internet Explorer'}}),
('5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 YaBrowser/16.2.0.1818 (beta) Safari/537.36',
    ('Linux', 'Yandex.Browser 16.2.0.1818'),
    {'os': {'name': 'Linux'}, 'bot': False, 'browser': {'version': '16.2.0.1818', 'name': 'Yandex.Browser'}}),
('Mozilla/5.0 (Linux; Android 8.0.0; Nexus 5X Build/OPR6.170623.023) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
    ('Android Linux 8.0.0', 'Chrome 62.0.3202.84'),
    {'bot': False, 'browser': {'name': 'Chrome', 'version': '62.0.3202.84'}, 'dist': {'name': 'Android', 'version': '8.0.0'}, 'os': {'name': 'Linux'}}),
('Mozilla/5.0 (Android 6.0.1; Mobile; rv:63.0) Gecko/63.0 Firefox/63.0',
    ('Android 6.0.1', 'Firefox 63.0'),
    {'dist': {'name': 'Android', 'version': '6.0.1'}, 'bot': False, 'browser': {'name': 'Firefox', 'version': '63.0'}}),
('Mozilla/5.0 (Linux; Android 8.1.0) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.111 Mobile Safari/537.36',
    ('Android Linux 8.1.0', 'Chrome 76.0.3809.111'),
    {'os': {'name': 'Linux'}, 'bot': False, 'dist': {'version': '8.1.0', 'name': 'Android'}, 'browser': {'version': '76.0.3809.111', 'name': 'Chrome'}}),
("Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/102.0 Mobile/15E148 Safari/605.1.15",
    ('iPhone iOS 12.4', 'Firefox 102.0'),
    {'os': {'name': 'iOS'}, "dist": {'name': 'iPhone', 'version': '12.4'}, 'bot': False, 'browser': {'name': 'Firefox', 'version': '102.0'}}),
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
        self.assertEqual(result['os']['name'], None)
        self.assertEqual(result['browser']['version'], None)
        result = detect('Linux; Android', fill_none=True)
        self.assertEqual(result['os']['name'], 'Linux')
        self.assertEqual(result['os']['version'], None)
        self.assertEqual(result['browser']['name'], 'AndroidBrowser')
        self.assertEqual(result['browser']['version'], None)

if __name__ == '__main__':
    unittest.main()
