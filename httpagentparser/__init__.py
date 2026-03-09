"""
Extract client information from http user agent
The module does not try to detect all capabilities of browser in current form (it can easily be extended though).
Tries to
    * be fast
    * very easy to extend
    * reliable enough for practical purposes
    * assist python web apps to detect clients.
"""

__version__ = '1.9.9'


class DetectorsHub(dict):
    _known_types = ['os', 'dist', 'flavor', 'browser']

    def __init__(self, *args, **kw):
        dict.__init__(self, *args, **kw)
        for typ in self._known_types:
            self.setdefault(typ, [])
        self.registerDetectors()

    def register(self, detector):
        if detector.info_type not in self._known_types:
            self[detector.info_type] = [detector]
            self._known_types.insert(detector.order, detector.info_type)
        else:
            self[detector.info_type].append(detector)

    def __iter__(self):
        return iter(self._known_types)

    def registerDetectors(self):
        detectors = [v() for v in list(globals().values()) if DetectorBase in getattr(v, '__mro__', [])]
        for d in detectors:
            if d.can_register:
                self.register(d)


class DetectorBase(object):
    name = ""  # "to perform match in DetectorsHub object"
    info_type = "override me"
    result_key = "override me"
    order = 10  # 0 is highest
    look_for = "string to look for"
    skip_if_found = []  # strings if present stop processin
    can_register = False
    version_markers = [("/", " ")]
    allow_space_in_version = False
    _suggested_detectors = None
    platform = None
    bot = False
    model = ""

    def __init__(self):
        if not self.name:
            self.name = self.__class__.__name__
        self.can_register = (self.__class__.__dict__.get('can_register', True))

        if isinstance(self.look_for, (tuple, list)):
            self._look_for = self.look_for
        else:
            self._look_for = (self.look_for,)

        if isinstance(self.version_markers[0], (list, tuple)):
            self._version_markers = self.version_markers
        else:
            self._version_markers = [self.version_markers]

    def detect(self, agent, result):
        # -> True/None
        word = self.checkWords(agent)
        if word:
            result[self.info_type] = dict(name=self.name)
            result['bot'] = self.bot
            version = self.getVersion(agent, word)
            if version:
                result[self.info_type]['version'] = version
            if self.platform:
                result['platform'] = {'name': self.platform, 'version': version}
            result['model'] = self.getModel(agent, word)

            return True

    def checkWords(self, agent):
        # -> True/None
        for w in self.skip_if_found:
            if w in agent:
                return False
        for word in self._look_for:
            if word in agent:
                return word

    def getVersion(self, agent, word):
        """
        => version string /None
        """
        version_part = agent.split(word, 1)[-1]
        for start, end in self._version_markers:
            if version_part.startswith(start) and end in version_part:
                version = version_part[1:]
                if end:  # end could be empty string
                    version = version.split(end)[0]
                if not self.allow_space_in_version:
                    version = version.split()[0]
                return version

    def getModel(self, agent, word):
        """
        => model string /None
        """
        model_markers = self.model_markers if \
            isinstance(self.model_markers[0], (list, tuple)) else [self.model_markers]
        model_part = model.split(word, 1)[-1]
        for start, end in model_markers:
            if model_part.startswith(start) and end in model_part:
                model = model_part[1:]
                if end:  # end could be empty string
                    model = model.split(end)[0]
                if not self.allow_space_in_model:
                    model = model.split()[0]
                return model


class OS(DetectorBase):
    info_type = "os"
    can_register = False
    version_markers = [";", " "]
    allow_space_in_version = True
    platform = None


class Dist(DetectorBase):
    info_type = "dist"
    can_register = False
    platform = None


class Flavor(DetectorBase):
    info_type = "flavor"
    can_register = False
    platform = None


class Browser(DetectorBase):
    info_type = "browser"
    can_register = False


class Konqueror(Browser):
    look_for = "Konqueror"
    version_markers = ["/", ";"]


class OperaMobile(Browser):
    look_for = "Opera Mobi"
    name = "Opera Mobile"

    def getVersion(self, agent, word):
        try:
            look_for = "Version"
            return agent.split(look_for)[1][1:].split(' ')[0]
        except IndexError:
            look_for = "Opera"
            return agent.split(look_for)[1][1:].split(' ')[0]


class Opera(Browser):
    look_for = "Opera"
    skip_if_found = ['Opera Mobi']

    def getVersion(self, agent, word):
        try:
            look_for = "Version"
            return agent.split(look_for)[1][1:].split(' ')[0]
        except IndexError:
            look_for = "Opera"
            version = agent.split(look_for)[1][1:].split(' ')[0]
            return version.split('(')[0]


class OperaNew(Browser):
    """
    Opera after version 15
    """
    name = "Opera"
    look_for = "OPR"
    skip_if_found = ["Build/OPR"]
    version_markers = [('/', '')]


class OperaGX(Browser):
    look_for = ["OPX", "OperaGX"]
    version_markers = ["/", ""]


class Netscape(Browser):
    look_for = "Netscape"
    version_markers = [("/", '')]


class Trident(Browser):
    look_for = "Trident"
    skip_if_found = ["MSIE", "Opera"]
    name = "Microsoft Internet Explorer"
    version_markers = ["/", ";"]
    trident_to_ie_versions = {
        '4.0': '8.0',
        '5.0': '9.0',
        '6.0': '10.0',
        '7.0': '11.0',
    }

    def getVersion(self, agent, word):
        return self.trident_to_ie_versions.get(super(Trident, self).getVersion(agent, word))


class MSIE(Browser):
    look_for = "MSIE"
    skip_if_found = ["Opera"]
    name = "Microsoft Internet Explorer"
    version_markers = [" ", ";"]


class MSEdge(Browser):
    look_for = "Edge"
    skip_if_found = ["MSIE"]
    version_markers = ["/", ""]


class ChromiumEdge(Browser):
    look_for = "Edg/"

    def getVersion(self, agent, word):
        if "Edg/" in agent:
            return agent.split('Edg/')[-1].split(' ')[0].strip()


class Galeon(Browser):
    look_for = "Galeon"


class WOSBrowser(Browser):
    look_for = "wOSBrowser"

    def getVersion(self, agent, word):
        pass


class Safari(Browser):
    look_for = "Safari"
    skip_if_found = ["Edge", "YaBrowser", "FxiOS"]

    def checkWords(self, agent):
        unless_list = ["Chrome", "OmniWeb", "wOSBrowser", "Android", "CriOS", "OPX", "Ddg"]
        if self.look_for in agent:
            for word in unless_list:
                if word in agent:
                    return False
            return self.look_for

    def getVersion(self, agent, word):
        if "Version/" in agent:
            return agent.split('Version/')[-1].split(' ')[0].strip()
        if "Safari/" in agent:
            return agent.split('Safari/')[-1].split(' ')[0].strip()
        else:
            return agent.split('Safari ')[-1].split(' ')[0].strip()  # Mobile Safari


class GoogleBot(Browser):
    # https://support.google.com/webmasters/answer/1061943
    look_for = ["Googlebot", "Googlebot-News", "Googlebot-Image",
                "Googlebot-Video", "Googlebot-Mobile", "Mediapartners-Google",
                "Mediapartners", "AdsBot-Google", "web/snippet"]
    bot = True
    version_markers = [('/', ';'), ('/', ' ')]


class GoogleFeedFetcher(Browser):
    look_for = "Feedfetcher-Google"
    bot = True

    def getVersion(self, agent, word):
        pass


class RunscopeRadar(Browser):
    look_for = "runscope-radar"
    bot = True


class GoogleAppEngine(Browser):
    look_for = "AppEngine-Google"
    bot = True

    def getVersion(self, agent, word):
        pass


class GoogleApps(Browser):
    look_for = "GoogleApps script"
    bot = True

    def getVersion(self, agent, word):
        pass


class TwitterBot(Browser):
    look_for = "Twitterbot"
    bot = True


class TelegramBot(Browser):
    look_for = "TelegramBot"
    bot = True


class MJ12Bot(Browser):
    look_for = "MJ12bot"
    bot = True


class YandexBot(Browser):
    # http://help.yandex.com/search/robots/agent.xml
    look_for = "Yandex"
    bot = True

    def getVersion(self, agent, word):
        return agent[agent.index('Yandex'):].split('/')[1].replace(')', ';').split(';')[0].strip()


class AmazonBot(Browser):
    look_for = "Amazonbot"
    version_markers = ["/", ";"]
    bot = True


class BingBot(Browser):
    look_for = "bingbot"
    version_markers = ["/", ";"]
    bot = True


class BaiduBot(Browser):
    # http://help.baidu.com/question?prod_en=master&class=1&id=1000973
    look_for = ["Baiduspider", "Baiduspider-image", "Baiduspider-video",
                "Baiduspider-news", "Baiduspider-favo", "Baiduspider-cpro",
                "Baiduspider-ads"]
    bot = True
    version_markers = ('/', ';')


class LinkedInBot(Browser):
    look_for = "LinkedInBot"
    bot = True


class ArchiveDotOrgBot(Browser):
    look_for = "archive.org_bot"
    bot = True


class YoudaoBot(Browser):
    look_for = "YoudaoBot"
    bot = True


class YoudaoBotImage(Browser):
    look_for = "YodaoBot-Image"
    bot = True


class RogerBot(Browser):
    look_for = "rogerbot"
    bot = True


class TweetmemeBot(Browser):
    look_for = "TweetmemeBot"
    bot = True


class WebshotBot(Browser):
    look_for = "WebshotBot"
    bot = True


class SensikaBot(Browser):
    look_for = "SensikaBot"
    bot = True


class YesupBot(Browser):
    look_for = "YesupBot"
    bot = True


class DotBot(Browser):
    look_for = "DotBot"
    bot = True


class PhantomJS(Browser):
    look_for = "Browser/Phantom"
    bot = True


class FacebookExternalHit(Browser):
    look_for = 'facebookexternalhit'
    bot = True


class SevenSiters(Browser):
    look_for = ["7Siters"]
    bot = True
    version_markers = [('/', ';')]


class NokiaOvi(Browser):
    look_for = "S40OviBrowser"


class UCBrowser(Browser):
    look_for = "UCBrowser"


class BrowserNG(Browser):
    look_for = "BrowserNG"


class Dolfin(Browser):
    look_for = 'Dolfin'


class NetFront(Browser):
    look_for = 'NetFront'


class Jasmine(Browser):
    look_for = 'Jasmine'


class Openwave(Browser):
    look_for = 'Openwave'


class UPBrowser(Browser):
    look_for = 'UP.Browser'


class OneBrowser(Browser):
    look_for = 'OneBrowser'


class ObigoInternetBrowser(Browser):
    look_for = 'ObigoInternetBrowser'


class TelecaBrowser(Browser):
    look_for = 'TelecaBrowser'


class MAUI(Browser):
    look_for = 'Browser/MAUI'

    def getVersion(self, agent, word):
        version = agent.split("Release/")[-1][:10]
        return version


class NintendoBrowser(Browser):
    look_for = 'NintendoBrowser'


class AndroidBrowser(Browser):
    look_for = "Android"
    skip_if_found = ['Chrome', 'Windows Phone', 'Opera', 'Firefox']

    # http://decadecity.net/blog/2013/11/21/android-browser-versions
    def getVersion(self, agent, word):
        pass


class Firefox(Browser):
    look_for = ["Firefox", "FxiOS"]
    version_markers = [('/', '')]
    skip_if_found = ["SeaMonkey", "web/snippet"]


class Firebird(Browser):
    look_for = ["Firebird"]
    version_markers = [('/', '')]


class Thunderbird(Browser):
    look_for = ["Thunderbird"]
    version_markers = [('/', '')]


class SeaMonkey(Browser):
    look_for = "SeaMonkey"
    version_markers = [('/', '')]


class iCanvas(Browser):
    look_for = "iCanvas"
    version_markers = ["/", ""]


class GuardianBrowser(Browser):
    look_for = "GuardianBrowser"
    version_markers = ["/", ""]


class DuckDuckGo(Browser):
    look_for = "Ddg"
    version_markers = ["/", ""]


class AsyncIO(Browser):
    look_for = ["aiohttp"]

    def getVersion(self, agent, word):
        return agent.split(word)[-1].split(')')[0].strip()


class Python(Browser):
    look_for = ["python", 'python-requests']
    skip_if_found = ['aiohttp']

    def getVersion(self, agent, word):
        return agent.split("/")[-1]


class Java(Browser):
    look_for = ["Java", "Java-http-client"]

    def getVersion(self, agent, word):
      if 'Java ' in agent:
        return agent.split('Java ')[-1].split(';')[0].strip()
      else:
        return agent.split("/")[-1]


class Curl(Browser):
    look_for = ["curl"]

    def getVersion(self, agent, word):
        return agent.split("/")[1].split(' ')[0].strip()


class Roku(Dist):
    look_for = ["Roku/DVP-", "RokuOS", "ROKU"]
    platform = 'Linux'

    def getVersion(self, agent, word):
      if 'Roku/DVP-' in agent:
          return agent.split('(')[-1].split(')')[0].strip()
      elif 'RokuOS' in agent:
          return agent.split('/')[-1].split(',')[0].strip()
      elif 'ROKU;' in agent:
          return agent.split('ROKU;')[-1].split(';')[0].strip()
      else:
        return 'Unknown'


class NetFlix(Browser):
    look_for = ["Netflix/"]

    device_versions = {
        "LGTV" : "LG TV",
        "NFANDROID2-PRV-FIRETVSTICK2016" : "Fire TV Stick 2016",
        "NFANDROID2-PRV-FIRETVSTICKPLUS2020" : "Fire TV Stick 2020",
        "NFANDROID2-PRV-FTVEAML950X4FHD2022" : "Fire TV Stick 2022 HD",
        "NFANDROID2-PRV-FTVEAML950X4HD2022" : "Fire TV Stick 2022 HD",
        "NFANDROID2-PRV-FIRETVN" : "Fire TV",
        "NFANDROID2-PRV-FTV" : "Fire TV",
        "RKU-381XX-" : "Roku Stream Stick 381xx (6th Gen)",
        "RKU-392XX-" : "Roku Premiere 392xx",
        "RKU-393XX-" : "Roku Express HD Streaming media Player 393xx",
        "RKU-39XXX-" : "Roku Express HD Streaming media Player 39xxx",
        "RKU-42XXX-" : "Roku 3 Media Streamer 4200X",
        "RKU-467XX-" : "Roku Ultra 467XX",
        "RKU-5XXXX-" : "Roku 5 Media Streamer 5000X",
        "RKU-" : "Ruku",
        "VIZMG152UI" : "Vizio M Series G1 52in TV",
        "VIZMG155UI" : "Vizio M Series G1 55in TV",
        "VIZ" : "Vizio TV",
        }

    def getVersion(self, agent, word):
        return agent.split("Netflix/")[-1].split(' ')[0].strip()

    def getModel(self, agent, word):
        model = 'Unknown'
        if 'DEVTYPE=' in agent:
          m = agent.split('DEVTYPE=')[-1].split(';')[0]
          for key in self.device_versions.keys():
            model = 'Unknown: ' + m
            if m in key:
              return self.device_versions.get(key)
          values = {key: value for key, value in self.device_versions.items() if key in m}
          #grab just the first value in case it is an empty dictionary and if so set to 'unknown'
          model = next(iter(values.values()), None)
          if model == None:
            model = 'Unknown: ' + m
        return model


class Darwin(OS):
    look_for = 'Darwin'
    platform = 'Darwin'
    version_markers = [("/", "")]

    darwin_versions = {
        #https://theapplewiki.com/wiki/Kernel#Versions
        "23.0.0" : "Mac OS X 14.0 / iOS 17.0",
        "23.1.0" : "Mac OS X 14.1 / iOS 17.1",
        "23.2.0" : "Mac OS X 14.2 / iOS 17.2",
        "23.3.0" : "Mac OS X 14.3 / iOS 17.3",
        "23.4.0" : "Mac OS X 14.4 / iOS 17.4",
        "23.5.0" : "Mac OS X 14.5 / iOS 17.5",
        "23.6.0" : "Mac OS X 14.6 - 14.8.3 / iOS 17.6 - 17.7.10",
        "24.0.0" : "Mac OS X 15.0 / iOS 18.0",
        "24.1.0" : "Mac OS X 15.1 / iOS 18.1",
        "24.2.0" : "Mac OS X 15.2 / iOS 18.2",
        "24.3.0" : "Mac OS X 15.3 / iOS 18.3",
        "24.4.0" : "Mac OS X 15.4 / iOS 18.4",
        "24.5.0" : "Mac OS X 15.5 / iOS 18.5",
        "24.6.0" : "Mac OS X 15.6 - 15.7.4 / iOS 18.6 - 18.7.3",
        "25.0.0" : "Mac OS X / iOS 26.0",
        "25.1.0" : "Mac OS X / iOS 26.1",
        "25.2.0" : "Mac OS X / iOS 26.2",
        "25.3.0" : "Mac OS X / iOS 26.3"
        }

    def getVersion(self, agent, word):
      if 'Darwin/' in agent:
        v = agent.split('Darwin/')[-1]
        return self.darwin_versions.get(v, 'Mac OS X / iOS - ' + v)
      elif '(Darwin ' in agent:
        v = agent.split('(Darwin ')[-1].split(' ')[0].strip()
        return self.darwin_versions.get(v, 'Mac OS X / iOS - ' + v)


class Linux(OS):
    look_for = 'Linux'
    platform = 'Linux'

    def getVersion(self, agent, word):
      if 'Linux ' in agent:
        return agent.split('Linux ')[-1].split(';')[0].split(')')[0].strip()
      elif 'Linux/' in agent:
        return agent.split('Linux/')[-1].replace(')', ' ').split(' ')[0].strip()
      elif 'Linux-' in agent:
        return agent.split('Linux-')[-1].split(';')[0].strip()


class Blackberry(OS):
    look_for = 'BlackBerry'
    platform = 'BlackBerry'

    def getVersion(self, agent, word):
        pass


class BlackberryPlaybook(Dist):
    look_for = 'PlayBook'
    platform = 'BlackBerry'

    def getVersion(self, agent, word):
        pass


class WindowsPhone(OS):
    name = "Windows Phone"
    platform = 'Windows'
    look_for = ["Windows Phone OS", "Windows Phone"]
    version_markers = [(" ", ";"), (" ", ")")]


class iOS(OS):
    look_for = ('iPhone', 'iPad', 'iPod', 'iOS', 'IOS,', 'Apple TVOS', 'Watch OS', 'watchOS')
    skip_if_found = ['like iPhone', 'Darwin']
    #some bugs get introduced with below, but better some noise than no IOS version detection.  May need to call getVersion and write that instead.
    version_markers = [("/", " "), ("/", ""), (" ", ";"), (" ", ")")]


class iPhone(Dist):
    look_for = 'iPhone'
    platform = 'iOS'
    skip_if_found = ['like iPhone', 'iPad', 'iPod']

    iphone_versions = {
        #https://gist.github.com/adamawolf/3048717
        "iPhone1,1" : "iPhone",
        "iPhone1,2" : "iPhone 3G",
        "iPhone2,1" : "iPhone 3GS",
        "iPhone3,1" : "iPhone 4",
        "iPhone3,2" : "iPhone 4 GSM Rev A",
        "iPhone3,3" : "iPhone 4 CDMA",
        "iPhone4,1" : "iPhone 4S",
        "iPhone5,1" : "iPhone 5 (GSM)",
        "iPhone5,2" : "iPhone 5 (GSM+CDMA)",
        "iPhone5,3" : "iPhone 5C (GSM)",
        "iPhone5,4" : "iPhone 5C (Global)",
        "iPhone6,1" : "iPhone 5S (GSM)",
        "iPhone6,2" : "iPhone 5S (Global)",
        "iPhone7,1" : "iPhone 6 Plus",
        "iPhone7,2" : "iPhone 6",
        "iPhone8,1" : "iPhone 6s",
        "iPhone8,2" : "iPhone 6s Plus",
        "iPhone8,4" : "iPhone SE (GSM)",
        "iPhone9,1" : "iPhone 7",
        "iPhone9,2" : "iPhone 7 Plus",
        "iPhone9,3" : "iPhone 7",
        "iPhone9,4" : "iPhone 7 Plus",
        "iPhone10,1" : "iPhone 8",
        "iPhone10,2" : "iPhone 8 Plus",
        "iPhone10,3" : "iPhone X Global",
        "iPhone10,4" : "iPhone 8",
        "iPhone10,5" : "iPhone 8 Plus",
        "iPhone10,6" : "iPhone X GSM",
        "iPhone11,2" : "iPhone XS",
        "iPhone11,4" : "iPhone XS Max",
        "iPhone11,6" : "iPhone XS Max Global",
        "iPhone11,8" : "iPhone XR",
        "iPhone12,1" : "iPhone 11",
        "iPhone12,3" : "iPhone 11 Pro",
        "iPhone12,5" : "iPhone 11 Pro Max",
        "iPhone12,8" : "iPhone SE 2nd Gen",
        "iPhone13,1" : "iPhone 12 Mini",
        "iPhone13,2" : "iPhone 12",
        "iPhone13,3" : "iPhone 12 Pro",
        "iPhone13,4" : "iPhone 12 Pro Max",
        "iPhone14,2" : "iPhone 13 Pro",
        "iPhone14,3" : "iPhone 13 Pro Max",
        "iPhone14,4" : "iPhone 13 Mini",
        "iPhone14,5" : "iPhone 13",
        "iPhone14,6" : "iPhone SE 3rd Gen",
        "iPhone14,7" : "iPhone 14",
        "iPhone14,8" : "iPhone 14 Plus",
        "iPhone15,2" : "iPhone 14 Pro",
        "iPhone15,3" : "iPhone 14 Pro Max",
        "iPhone15,4" : "iPhone 15",
        "iPhone15,5" : "iPhone 15 Plus",
        "iPhone16,1" : "iPhone 15 Pro",
        "iPhone16,2" : "iPhone 15 Pro Max",
        "iPhone17,1" : "iPhone 16 Pro",
        "iPhone17,2" : "iPhone 16 Pro Max",
        "iPhone17,3" : "iPhone 16",
        "iPhone17,4" : "iPhone 16 Plus",
        "iPhone17,5" : "iPhone 16e",
        "iPhone18,1" : "iPhone 17 Pro",
        "iPhone18,2" : "iPhone 17 Pro Max",
        "iPhone18,3" : "iPhone 17",
        "iPhone18,4" : "iPhone Air"
         }

    def getVersion(self, agent, word):
        if "iPhone/iOS" in agent:
            return agent.split('iPhone/iOS ')[-1].replace('_', '.').strip()
        elif "iPhone/" in agent:
            return agent.split('iPhone/')[-1].split(' ')[0].replace('_', '.').strip()
        elif "(iPhone; iOS" in agent:
            return agent.split('iPhone; iOS')[-1].split(';')[0].replace('_', '.').strip()
        elif "OS," in agent:
            return agent.split('OS,')[-1].split(',')[0].replace('_', '.').strip()
        elif "osVer/" in agent:
            return agent.split('osVer/')[-1].split(' ')[0].replace('_', '.').strip()
        elif "iOS; " in agent:
            return agent.split('iOS; ')[-1].split(';')[0].replace('_', '.').strip()
        elif "; iOS " in agent:
            return agent.split('; iOS ')[-1].split(';')[0].replace('_', '.').strip()
        elif ("iOS/" in agent) and ("CriOS" not in agent) and ("EdgiOS" not in agent) and ("FxiOS" not in agent):
            return agent.split('iOS/')[-1].split(' ')[0].replace('_', '.').strip()
        elif "ios-iphone;" in agent:
            return agent.split('ios-iphone;')[-1].split(';')[0].replace('_', '.').strip()
        elif "; CPU OS " in agent:
            return agent.split('; CPU OS ')[-1].split(';')[0].replace('_', '.').strip()
        elif "iPhone OS " in agent:
          return agent.split('iPhone OS ')[-1].split(' ')[0].replace('_', '.').strip()
        else:
          return None

    def getModel(self, agent, word):
        if '(iPhone' in agent:
          m = "iPhone" + agent.split('(iPhone')[-1].replace(')', ';').split(';')[0]
          return self.iphone_versions.get(m, 'Unknown')
        elif ',iPhone' in agent:
          m = "iPhone" + agent.split(',iPhone')[-1].split(']')[0]
          return self.iphone_versions.get(m, 'Unknown')
        elif '; iPhone' in agent:
          m = "iPhone" + agent.split('; iPhone')[-1].split(';')[0]
          return self.iphone_versions.get(m, 'Unknown')
        elif 'hw/iPhone' in agent:
          m = "iPhone" + agent.replace('_', ',').split('hw/iPhone')[-1].split(']')[0]
          m = self.iphone_versions.get(m, 'Unknown')
          return m
        elif ';ios-iphone;' in agent:
          m = agent.split(';ios-iphone;')[0].split(';')[-1]
          return m
        elif 'model/' in agent:
          m = agent.split('model/')[-1].split('/')[0]
          if m.startswith('iPhone '):
            i = m.rfind(' ')
            return m[0:i]
          else:
            m = m.split('model/')[-1].split(' ')[0]
            return self.iphone_versions.get(m, 'Unknown')
        else:
          return 'Unknown'



class IPad(Dist):
    look_for = 'iPad'
    platform = 'iOS'

    ipad_versions = {
        #https://gist.github.com/adamawolf/3048717
        "iPad1,1" : "iPad",
        "iPad1,2" : "iPad 3G",
        "iPad2,1" : "2nd Gen iPad",
        "iPad2,2" : "2nd Gen iPad GSM",
        "iPad2,3" : "2nd Gen iPad CDMA",
        "iPad2,4" : "2nd Gen iPad New Revision",
        "iPad3,1" : "3rd Gen iPad",
        "iPad3,2" : "3rd Gen iPad CDMA",
        "iPad3,3" : "3rd Gen iPad GSM",
        "iPad2,5" : "iPad mini",
        "iPad2,6" : "iPad mini GSM+LTE",
        "iPad2,7" : "iPad mini CDMA+LTE",
        "iPad3,4" : "4th Gen iPad",
        "iPad3,5" : "4th Gen iPad GSM+LTE",
        "iPad3,6" : "4th Gen iPad CDMA+LTE",
        "iPad4,1" : "iPad Air (WiFi)",
        "iPad4,2" : "iPad Air (GSM+CDMA)",
        "iPad4,3" : "1st Gen iPad Air (China)",
        "iPad4,4" : "iPad mini Retina (WiFi)",
        "iPad4,5" : "iPad mini Retina (GSM+CDMA)",
        "iPad4,6" : "iPad mini Retina (China)",
        "iPad4,7" : "iPad mini 3 (WiFi)",
        "iPad4,8" : "iPad mini 3 (GSM+CDMA)",
        "iPad4,9" : "iPad Mini 3 (China)",
        "iPad5,1" : "iPad mini 4 (WiFi)",
        "iPad5,2" : "iPad mini 4 (WiFi+Cellular)",
        "iPad5,3" : "iPad Air 2 (WiFi)",
        "iPad5,4" : "iPad Air 2 (Cellular)",
        "iPad6,3" : "iPad Pro (9.7 inch, WiFi)",
        "iPad6,4" : "iPad Pro (9.7 inch, WiFi+LTE)",
        "iPad6,7" : "iPad Pro (12.9 inch, WiFi)",
        "iPad6,8" : "iPad Pro (12.9 inch, WiFi+LTE)",
        "iPad6,11" : "iPad (2017)",
        "iPad6,12" : "iPad (2017)",
        "iPad7,1" : "iPad Pro 2nd Gen (WiFi)",
        "iPad7,2" : "iPad Pro 2nd Gen (WiFi+Cellular)",
        "iPad7,3" : "iPad Pro 10.5-inch 2nd Gen (WiFi)",
        "iPad7,4" : "iPad Pro 10.5-inch 2nd Gen (WiFi+Cellular)",
        "iPad7,5" : "iPad 6th Gen (WiFi)",
        "iPad7,6" : "iPad 6th Gen (WiFi+Cellular)",
        "iPad7,11" : "iPad 7th Gen 10.2-inch (WiFi)",
        "iPad7,12" : "iPad 7th Gen 10.2-inch (WiFi+Cellular)",
        "iPad8,1" : "iPad Pro 11 inch 3rd Gen (WiFi)",
        "iPad8,2" : "iPad Pro 11 inch 3rd Gen (1TB, WiFi)",
        "iPad8,3" : "iPad Pro 11 inch 3rd Gen (WiFi+Cellular)",
        "iPad8,4" : "iPad Pro 11 inch 3rd Gen (1TB, WiFi+Cellular)",
        "iPad8,5" : "iPad Pro 12.9 inch 3rd Gen (WiFi)",
        "iPad8,6" : "iPad Pro 12.9 inch 3rd Gen (1TB, WiFi)",
        "iPad8,7" : "iPad Pro 12.9 inch 3rd Gen (WiFi+Cellular)",
        "iPad8,8" : "iPad Pro 12.9 inch 3rd Gen (1TB, WiFi+Cellular)",
        "iPad8,9" : "iPad Pro 11 inch 4th Gen (WiFi)",
        "iPad8,10" : "iPad Pro 11 inch 4th Gen (WiFi+Cellular)",
        "iPad8,11" : "iPad Pro 12.9 inch 4th Gen (WiFi)",
        "iPad8,12" : "iPad Pro 12.9 inch 4th Gen (WiFi+Cellular)",
        "iPad11,1" : "iPad mini 5th Gen (WiFi)",
        "iPad11,2" : "iPad mini 5th Gen (WiFi+Cellular)",
        "iPad11,3" : "iPad Air 3rd Gen (WiFi)",
        "iPad11,4" : "iPad Air 3rd Gen (WiFi+Cellular)",
        "iPad11,6" : "iPad 8th Gen (WiFi)",
        "iPad11,7" : "iPad 8th Gen (WiFi+Cellular)",
        "iPad12,1" : "iPad 9th Gen (WiFi)",
        "iPad12,2" : "iPad 9th Gen (WiFi+Cellular)",
        "iPad14,1" : "iPad mini 6th Gen (WiFi)",
        "iPad14,2" : "iPad mini 6th Gen (WiFi+Cellular)",
        "iPad13,1" : "iPad Air 4th Gen (WiFi)",
        "iPad13,2" : "iPad Air 4th Gen (WiFi+Cellular)",
        "iPad13,4" : "iPad Pro 11 inch 5th Gen",
        "iPad13,5" : "iPad Pro 11 inch 5th Gen",
        "iPad13,6" : "iPad Pro 11 inch 5th Gen",
        "iPad13,7" : "iPad Pro 11 inch 5th Gen",
        "iPad13,8" : "iPad Pro 12.9 inch 5th Gen",
        "iPad13,9" : "iPad Pro 12.9 inch 5th Gen",
        "iPad13,10" : "iPad Pro 12.9 inch 5th Gen",
        "iPad13,11" : "iPad Pro 12.9 inch 5th Gen",
        "iPad13,16" : "iPad Air 5th Gen (WiFi)",
        "iPad13,17" : "iPad Air 5th Gen (WiFi+Cellular)",
        "iPad13,18" : "iPad 10th Gen (WiFi)",
        "iPad13,19" : "iPad 10th Gen (WiFi+Cellular)",
        "iPad14,3" : "iPad Pro 11 inch 4th Gen (WiFi)",
        "iPad14,4" : "iPad Pro 11 inch 4th Gen (WiFi+Cellular)",
        "iPad14,5" : "iPad Pro 12.9 inch 6th Gen (WiFi)",
        "iPad14,6" : "iPad Pro 12.9 inch 6th Gen (WiFi+Cellular)",
        "iPad14,8" : "iPad Air 11 inch 6th Gen (WiFi)",
        "iPad14,9" : "iPad Air 11 inch 6th Gen (WiFi+Cellular)",
        "iPad14,10" : "iPad Air 13 inch 6th Gen (WiFi)",
        "iPad14,11" : "iPad Air 13 inch 6th Gen (WiFi+Cellular)",
        "iPad15,3" : "iPad Air 11-inch 7th Gen (WiFi)",
        "iPad15,4" : "iPad Air 11-inch 7th Gen (WiFi+Cellular)",
        "iPad15,5" : "iPad Air 13-inch 7th Gen (WiFi)",
        "iPad15,6" : "iPad Air 13-inch 7th Gen (WiFi+Cellular)",
        "iPad15,7" : "iPad 11th Gen (WiFi)",
        "iPad15,8" : "iPad 11th Gen (WiFi+Cellular)",
        "iPad16,1" : "iPad mini 7th Gen (WiFi)",
        "iPad16,2" : "iPad mini 7th Gen (WiFi+Cellular)",
        "iPad16,3" : "iPad Pro 11 inch 5th Gen (WiFi)",
        "iPad16,4" : "iPad Pro 11 inch 5th Gen (WiFi+Cellular)",
        "iPad16,5" : "iPad Pro 12.9 inch 7th Gen (WiFi)",
        "iPad16,6" : "iPad Pro 12.9 inch 7th Gen (WiFi+Cellular)"
     }

    def getVersion(self, agent, word):
        version_end_chars = [' ']
        if "iPad/iPadOS" in agent:
            return agent.split('iPad/iPadOS ')[-1].replace('_', '.').strip()
        elif "iPad/" in agent:
            return agent.split('iPad/')[-1].split(' ')[0].replace('_', '.').strip()
        elif ("iOS/" in agent) and ("CriOS" not in agent) and ("EdgiOS" not in agent) and ("FxiOS" not in agent):
            return agent.split('iOS/')[-1].split(' ')[0].replace('_', '.').strip()
        elif "iPad; iOS " in agent:
            return agent.split('iPad; iOS ')[-1].split(';')[0].replace('_', '.').strip()
        elif "OS," in agent:
            return agent.split('OS,')[-1].split(',')[0].replace('_', '.').strip()
        elif "CPU Darwin " in agent:
            return agent.split('CPU Darwin ')[-1].split(' ')[0].replace('_', '.').strip()
        elif "CPU iPad OS " in agent:
          return agent.split('CPU iPad OS ')[-1].replace('_', '.').split(' ')[0].strip()
        elif "CPU OS " in agent:
          return agent.split('CPU OS ')[-1].replace('_', '.').strip()
        elif agent.startswith('iPad'):
          return agent.split('/')[-1].replace('_', '.').split(' ')[0]
        else:
          return None

    def getModel(self, agent, word):
        if '(iPad' in agent:
          m = "iPad" + agent.split('(iPad')[-1].replace(')', ';').split(';')[0]
          return self.ipad_versions.get(m, m)
        if ';iPad' in agent:
          m = "iPad" + agent.split(';iPad')[-1].replace(')', ';').split(';')[0]
          return self.ipad_versions.get(m, m)
        elif ',iPad' in agent:
          m = "iPad" + agent.split(',iPad')[-1].split(']')[0]
          return self.ipad_versions.get(m, 'Unknown')
        elif 'hw/iPad' in agent:
          m = "iPad" + agent.replace('_', ',').split('hw/iPad')[-1].split(']')[0]
          return self.ipad_versions.get(m, 'Unknown')
        elif 'model/iPad' in agent:
          m = "iPad" + agent.split('model/iPad')[-1].split(' ')[0]
          return self.ipad_versions.get(m, 'Unknown')
        elif agent.startswith('iPad'):
          m = agent.split('/')[0]
          return self.ipad_versions.get(m, 'Unknown')
        else:
          return 'Unknown'


class IPod(Dist):
    look_for = ['iPod;', 'iPod/', 'iPod touch']
    platform = 'iOS'

    ipod_versions = {
        #https://gist.github.com/adamawolf/3048717
        "iPod1,1" : "1st Gen iPod",
        "iPod2,1" : "2nd Gen iPod",
        "iPod3,1" : "3rd Gen iPod",
        "iPod4,1" : "4th Gen iPod",
        "iPod5,1" : "5th Gen iPod",
        "iPod6,1" : "6th Gen iPod",
        "iPod7,1" : "7th Gen iPod"
        }

    def getVersion(self, agent, word):
        version_end_chars = [' ']
        if "iPad/iPadOS" in agent:
            return agent.split('iPad/iPadOS ')[-1].replace('_', '.').strip()
        elif "CPU OS " in agent:
            return agent.split('CPU OS ')[-1].replace('_', '.').strip()
        elif "iPhone OS " in agent:
          return agent.split('iPhone OS ')[-1].split(' ')[0].replace('_', '.').strip()
        else:
          return None

    def getModel(self, agent, word):
        m = "iPod" + agent.split('(iPod')[-1].split(';')[0]
        return self.ipod_versions.get(m, 'Unknown')


class AppleWatch(Dist):
    look_for = ['Watch OS', 'watchOS']
    platform = 'iOS'

    watchos_versions = {
        #https://gist.github.com/adamawolf/3048717
        "Watch1,1" : "Apple Watch 38mm case",
        "Watch1,2" : "Apple Watch 42mm case",
        "Watch2,6" : "Apple Watch Series 1 38mm case",
        "Watch2,7" : "Apple Watch Series 1 42mm case",
        "Watch2,3" : "Apple Watch Series 2 38mm case",
        "Watch2,4" : "Apple Watch Series 2 42mm case",
        "Watch3,1" : "Apple Watch Series 3 38mm case (GPS+Cellular)",
        "Watch3,2" : "Apple Watch Series 3 42mm case (GPS+Cellular)",
        "Watch3,3" : "Apple Watch Series 3 38mm case (GPS)",
        "Watch3,4" : "Apple Watch Series 3 42mm case (GPS)",
        "Watch4,1" : "Apple Watch Series 4 40mm case (GPS)",
        "Watch4,2" : "Apple Watch Series 4 44mm case (GPS)",
        "Watch4,3" : "Apple Watch Series 4 40mm case (GPS+Cellular)",
        "Watch4,4" : "Apple Watch Series 4 44mm case (GPS+Cellular)",
        "Watch5,1" : "Apple Watch Series 5 40mm case (GPS)",
        "Watch5,2" : "Apple Watch Series 5 44mm case (GPS)",
        "Watch5,3" : "Apple Watch Series 5 40mm case (GPS+Cellular)",
        "Watch5,4" : "Apple Watch Series 5 44mm case (GPS+Cellular)",
        "Watch5,9" : "Apple Watch SE 40mm case (GPS)",
        "Watch5,10" : "Apple Watch SE 44mm case (GPS)",
        "Watch5,11" : "Apple Watch SE 40mm case (GPS+Cellular)",
        "Watch5,12" : "Apple Watch SE 44mm case (GPS+Cellular)",
        "Watch6,1" : "Apple Watch Series 6 40mm case (GPS)",
        "Watch6,2" : "Apple Watch Series 6 44mm case (GPS)",
        "Watch6,3" : "Apple Watch Series 6 40mm case (GPS+Cellular)",
        "Watch6,4" : "Apple Watch Series 6 44mm case (GPS+Cellular)",
        "Watch6,6" : "Apple Watch Series 7 41mm case (GPS)",
        "Watch6,7" : "Apple Watch Series 7 45mm case (GPS)",
        "Watch6,8" : "Apple Watch Series 7 41mm case (GPS+Cellular)",
        "Watch6,9" : "Apple Watch Series 7 45mm case (GPS+Cellular)",
        "Watch6,10" : "Apple Watch SE 40mm case (GPS)",
        "Watch6,11" : "Apple Watch SE 44mm case (GPS)",
        "Watch6,12" : "Apple Watch SE 40mm case (GPS+Cellular)",
        "Watch6,13" : "Apple Watch SE 44mm case (GPS+Cellular)",
        "Watch6,14" : "Apple Watch Series 8 41mm case (GPS)",
        "Watch6,15" : "Apple Watch Series 8 45mm case (GPS)",
        "Watch6,16" : "Apple Watch Series 8 41mm case (GPS+Cellular)",
        "Watch6,17" : "Apple Watch Series 8 45mm case (GPS+Cellular)",
        "Watch6,18" : "Apple Watch Ultra",
        "Watch7,1" : "Apple Watch Series 9 41mm case (GPS)",
        "Watch7,2" : "Apple Watch Series 9 45mm case (GPS)",
        "Watch7,3" : "Apple Watch Series 9 41mm case (GPS+Cellular)",
        "Watch7,4" : "Apple Watch Series 9 45mm case (GPS+Cellular)",
        "Watch7,5" : "Apple Watch Ultra 2",
        "Watch7,8" : "Apple Watch Series 10 42mm case (GPS)",
        "Watch7,9" : "Apple Watch Series 10 46mm case (GPS)",
        "Watch7,10" : "Apple Watch Series 10 42mm case (GPS+Cellular)",
        "Watch7,11" : "Apple Watch Series 10 46mm case (GPS+Cellular)",
        "Watch7,12" : "Apple Watch Ultra 3 49mm case",
        "Watch7,13" : "Apple Watch SE 3 40mm case",
        "Watch7,14" : "Apple Watch SE 3 44mm case",
        "Watch7,15" : "Apple Watch SE 3 40mm case (GPS+Cellular)",
        "Watch7,16" : "Apple Watch SE 3 44mm case (GPS+Cellular)",
        "Watch7,17" : "Apple Watch Series 11 42mm case",
        "Watch7,18" : "Apple Watch Series 11 46mm case",
        "Watch7,19" : "Apple Watch Series 11 42mm case (GPS+Celllular)",
        "Watch7,20" : "Apple Watch Series 11 46mm case (GPS+Celllular)"
        }

    def getVersion(self, agent, word):
        if "OS," in agent:
            return agent.split('OS,')[-1].split(',')[0].strip()
        if "watchOS " in agent:
            return agent.split('watchOS ')[-1].split(';')[0].strip()

    def getModel(self, agent, word):
        if ',Watch' in agent:
          m = "Watch" + agent.split(',Watch')[-1].split(']')[0]
          return self.watchos_versions.get(m, 'Unknown')
        else:
          return 'Unknown'


class AppleTV(Dist):
    look_for = 'Apple TVOS'
    platform = 'iOS'

    tv_versions = {
        #https://theapplewiki.com/wiki/List_of_Apple_TVs
        "AppleTV1,1" : "Apple TV 1st Gen",
        "AppleTV2,1" : "Apple TV 2nd Gen",
        "AppleTV3,1" : "Apple TV 3rd Gen",
        "AppleTV3,2" : "Apple TV 3rd Gen",
        "AppleTV5,3" : "Apple TV HD",
        "AppleTV6,2" : "Apple TV 4K",
        "AppleTV11,1" : "Apple TV 4K 2nd Gen",
        "AppleTV14,1" : "Apple TV 4K 3rd Gen"
        }

    def getVersion(self, agent, word):
        if "OS," in agent:
            return agent.split('OS,')[-1].split(',')[0].strip()

    def getModel(self, agent, word):
        if ',AppleTV' in agent:
          m = "AppleTV" + agent.split(',AppleTV')[-1].split(']')[0]
          return self.tv_versions.get(m, 'Unknown')
        else:
          return 'Unknown'

class Macintosh(OS):
    look_for = ['Macintosh', '(Apple']
    skip_if_found = ['Apple Watch']

    def getVersion(self, agent, word):
      if "Silicon" in agent:
          return agent.split('Silicon')[-1].replace('_','.').split(')')[0].strip()
      elif "macOS " in agent:
          return agent.split('macOS ')[-1].split(';')[0].strip()



class MacOS(Flavor):
    look_for = ['Mac OS', 'MacOS', "Mac;", "macOS/", "macOS,", "(macOS", "Mac/", ".Mac", "OSX", "/macOS"]
    platform = 'Mac OS'
    skip_if_found = ['iPhone', 'iPad', 'iPod']

    mac_versions = {
        #https://support.apple.com/en-us/108052
        #https://appledb.dev/device-selection/Macs.html
        "iMac13,1" : "iMac (21.5-inch, 2012)",
        "iMac13,2" : "iMac (27-inch, 2012)",
        "iMac13,3" : "iMac (21.5-inch, 2013)",
        "iMac14,1" : "iMac (21.5-inch, 2013, Integrated Graphics)",
        "iMac14,2" : "iMac (27-inch, 2013)",
        "iMac14,3" : "iMac (21.5-inch, 2013, Dedicated Graphics)",
        "iMac14,4" : "iMac (21.5-inch, 2014)",
        "iMac15,1" : "iMac (Retina 5K, 27-inch, 2014 & 2015)",
        "iMac16,1" : "iMac (21.5-inch, 2015)",
        "iMac16,2" : "iMac (Retina 4K, 21.5-inch, 2015)",
        "iMac17,1" : "iMac (Retina 5K, 27-inch, 2015)",
        "iMac18,1" : "iMac (21.5-inch, 2017)",
        "iMac18,2" : "iMac (Retina 4K, 21.5-inch, 2017)",
        "iMac18,3" : "iMac (Retina 5K, 27-inch, 2017)",
        "iMac19,1" : "iMac (Retina 5K, 27-inch, 2019)",
        "iMac19,2" : "iMac (Retina 4K, 21.5-inch, 2019)",
        "iMac20,1" : "iMac (Retina 5K, 27-inch, 2020)",
        "iMac20,1" : "iMac (Retina 5K, 27-inch, 2020)",
        "iMac21,1" : "iMac (24-inch, M1, 2021)",
        "iMac21,2" : "iMac (24-inch, M1, 2021)",
        "MacBookAir6,1" : "MacBook Air (11-inch, 2014)",
        "MacBookAir6,2" : "MacBook Air (13-inch, 2014)",
        "MacBookAir7,1" : "MacBook Air (13-inch, 2015)",
        "MacBookAir7,2" : "MacBook Air (13-inch, 2015 & 2017)",
        "MacBookAir8,1" : "MacBook Air (Retina, 13-inch, 2018)",
        "MacBookAir8,2" : "MacBook Air (Retina, 13-inch, 2019)",
        "MacBookAir9,1" : "MacBook Air (Retina, 13-inch, 2020)",
        "MacBookAir10,1" : "MacBook Air (M1, 2020)",
        "MacBookPro9,1" : "MacBook Pro (15-inch, 2012)",
        "MacBookPro9,2" : "MacBook Pro (13-inch, 2012)",
        "MacBookPro10,1" : "MacBook Pro (Retina, 15-inch, 2012 & 2013)",
        "MacBookPro10,2" : "MacBook Pro (Retina, 13-inch, 2012 & 2013)",
        "MacBookPro11,1" : "MacBook Pro (Retina, 13-inch, 2014",
        "MacBookPro11,2" : "MacBook Pro (Retina, 15-inch, 2013 & 2014",
        "MacBookPro11,3" : "MacBook Pro (Retina, 13-inch, 2013 & 2014",
        "MacBookPro11,4" : "MacBook Pro (Retina, 15-inch, 2015",
        "MacBookPro11,5" : "MacBook Pro (Retina, 15-inch, 2015",
        "MacBookPro12,1" : "MacBook Pro (Retina, 13-inch, 2015",
        "MacBookPro13,1" : "MacBook Pro (15-inch, 2016",
        "MacBookPro13,2" : "MacBook Pro (13-inch, 2016",
        "MacBookPro13,3" : "MacBook Pro (13-inch, 2016",
        "MacBookPro14,1" : "MacBook Pro (13-inch, 2017, 2 Thunderbolt 3 ports)",
        "MacBookPro14,2" : "MacBook Pro (13-inch, 2017, 4 Thunderbolt 3 ports)",
        "MacBookPro14,3" : "MacBook Pro (15-inch, 2017)",
        "MacBookPro15,1" : "MacBook Pro (15-inch, 2018 & 2019)",
        "MacBookPro15,2" : "MacBook Pro (13-inch, 2018 & 2019, 4 Thunderbolt 3 ports)",
        "MacBookPro15,3" : "MacBook Pro (15-inch, 2019)",
        "MacBookPro15,4" : "MacBook Pro (13-inch, 2019, 2 Thunderbolt 3 ports)",
        "MacBookPro16,1" : "MacBook Pro (16-inch, 2019)",
        "MacBookPro16,2" : "MacBook Pro (13-inch, 2020, 4 Thunderbolt 3 ports)",
        "MacBookPro16,3" : "MacBook Pro (13-inch, 2020, 2 Thunderbolt 3 ports)",
        "MacBookPro16,4" : "MacBook Pro (16-inch, 2019)",
        "MacBookPro17,1" : "MacBook Pro (13-inch, M1, 2020)",
        "MacBookPro18,1" : "MacBook Pro (16-inch, 2021)",
        "MacBookPro18,2" : "MacBook Pro (16-inch, 2021)",
        "MacBookPro18,3" : "MacBook Pro (14-inch, 2021)",
        "MacBookPro18,4" : "MacBook Pro (14-inch, 2021)",
        "Macmini1,1" : "Mac mini (2006)",
        "Macmini2,1" : "Mac mini (2007)",
        "Macmini3,1" : "Mac mini (2009)",
        "Macmini4,1" : "Mac mini (2010)",
        "Macmini5,1" : "Mac mini (2011)",
        "Macmini5,2" : "Mac mini (2011)",
        "Macmini5,3" : "Mac mini (2011)",
        "Macmini6,1" : "Mac mini (2012)",
        "Macmini6,2" : "Mac mini (2012)",
        "Macmini7,1" : "Mac mini (2014)",
        "Macmini8,1" : "Mac mini (2018)",
        "Macmini9,1" : "Mac mini (M1, 2020)",
        "Mac14,2" : "MacBook Air (M2, 2022)",
        "Mac14,3" : "Mac Mini  (2023)",
        "Mac14,5" : "MacBook Pro (14-inch, 2023)",
        "Mac14,6" : "MacBook Pro (16-inch, 2023)",
        "Mac14,7" : "MacBook Pro (13-inch, M2, 2022)",
        "Mac14,8" : "Mac Pro (2023)",
        "Mac14,9" : "MacBook Pro (14-inch, 2023)",
        "Mac14,10" : "MacBook Pro (16-inch, 2023)",
        "Mac14,12" : "Mac Mini (2023)",
        "Mac14,13" : "Mac Studio (2023)",
        "Mac14,14" : "Mac Studio (2023)",
        "Mac14,15" : "MacBook Air (15-inch, M2, 2023)",
        "Mac15,1" : "iMac (Retina 5K, 27-inch, 2015)",
        "Mac15,3" : "MacBook Pro (14-inch, 2023)",
        "Mac15,4" : "iMac (24-inch, M3, 2023)",
        "Mac15,5" : "iMac (24-inch, M3, 2023)",
        "Mac15,6" : "MacBook Pro (14-inch, 2023)",
        "Mac15,7" : "MacBook Pro (16-inch, 2023)",
        "Mac15,8" : "MacBook Pro (14-inch, 2023)",
        "Mac15,9" : "MacBook Pro (16-inch, 2023)",
        "Mac15,10" : "MacBook Pro (14-inch, 2023)",
        "Mac15,11" : "MacBook Pro (16-inch, 2023)",
        "Mac15,12" : "MacBook Air (13-inch, M3, 2024)",
        "Mac15,13" : "MacBook Air (15-inch, M3, 2024)",
        "Mac15,14" : "Mac Studio (2025)",
        "Mac16,1" : "MacBook Pro (14-inch, 2024)",
        "Mac16,2" : "iMac (24-inch, M4, 2024)",
        "Mac16,3" : "iMac (24-inch, M4, 2024)",
        "Mac16,5" : "MacBook Pro (16-inch, 2024)",
        "Mac16,6" : "MacBook Pro (14-inch, 2024)",
        "Mac16,7" : "MacBook Pro (16-inch, 2024)",
        "Mac16,8" : "MacBook Pro (14-inch, 2024)",
        "Mac16,9" : "Mac Studio (2025)",
        "Mac16,10" : "Mac mini (2024)",
        "Mac16,11" : "Mac mini (2024)",
        "Mac16,12" : "MacBook Air (13-inch, M4, 2025)",
        "Mac16,13" : "MacBook Air (15-inch, M4, 2025)",
        "Mac17,2" : "MacBook Pro (14-inch, M5, 2025)",
        }


    def getVersion(self, agent, word):
        if 'Mac;OSX;' in agent:
          return agent.split('Mac;OSX;')[-1].split(' ')[0].replace('_', '.')
        elif 'OSX_' in agent:
          return agent.split('OSX_')[-1].split('/')[0].replace('_', '.')
        elif '/macOS' in agent:
          return agent.split('/macOS')[-1].replace('_', '.')
        elif 'macOS/' in agent:
          return agent.split('macOS/')[-1].split(' ')[0].replace('_', '.')
        elif 'Mac/' in agent:
          return agent.split('Mac/')[-1].replace('_', '.')
        elif '(macOS' in agent:
          return agent.split('(macOS')[-1].split('/')[0].split(';')[0].replace('_', '.').strip()
        elif "macOS," in agent:
            return agent.split('OS,')[-1].split(',')[0].replace('_', '.').strip()
        elif "[Mac OS X," in agent:
            return agent.split('[Mac OS X,')[-1].split(',')[0].replace('_', '.').strip()
        elif " Mac OS X " in agent:
            return agent.split(' Mac OS X ')[-1].split(';')[0].split(')')[0].replace('_', '.').strip()
        elif ";Mac OS X (" in agent:
            return agent.split(';Mac OS X (')[-1].split(')')[0].replace('_', '.').strip()
        elif ".Mac " in agent:
            return agent.split('.Mac ')[-1].split(' ')[0].replace('_', '.').strip()
        elif "Mac OS/" in agent:
            return agent.split('Mac OS/')[-1].split(';')[0].replace('_', '.').strip()
        else:
          return agent.split('Mac OS')[-1].replace('_', '.').strip()

    def getModel(self, agent, word):
        if ',Mac' in agent:
          #this works for Mac, MacBookPro, and MacBookAir
          m = "Mac" + agent.split(',Mac')[-1].split(']')[0]
          return self.mac_versions.get(m, 'Unknown: ' + m)
        elif ' Apple/' in agent:
          #this works for Mac, MacBookPro, and MacBookAir
          m = "Mac" + agent.split('Apple/Mac')[-1].split(')')[0]
          return self.mac_versions.get(m, 'Unknown: ' + m)
        elif ('(Mac' in agent) and ('Macintosh' not in agent):
          #this works for Mac, MacBookPro, and MacBookAir
          m = "Mac" + agent.split('(Mac')[-1].split(')')[0]
          return self.mac_versions.get(m, 'Unknown: ' + m)
        elif ',iMac' in agent:
          m = "iMac" + agent.split(',iMac')[-1].split(']')[0]
          return self.mac_versions.get(m, 'Unknown: ' + m)
        elif '; Mac OS X ' in agent:
          return agent.split('; Mac Mac OS X ')[-1].split(';')[-1].split(')')[0].strip()
        elif '; Mac' in agent:
          #this works for Mac, MacBookPro, and MacBookAir
          m = "Mac" + agent.split('; Mac')[-1].split(')')[0]
          return self.mac_versions.get(m, 'Unknown: ' + m)
        else:
          return 'Unknown'


class Windows(Dist):
    look_for = 'Windows'
    platform = 'Windows'


class Windows(OS):
    look_for = ['Windows', 'windows', '.Win ', 'Win32']
    platform = 'Windows'
    skip_if_found = ["Windows Phone"]
    win_versions = {
                    "26200": "11 - 25H2",
                    "26100": "11 - 24H2",
                    "22631": "11 - 23H2",
                    "22621": "11 - 22H2",
                    "22000": "11 - 21H2",
                    "Windows 11": "11",
                    "NT 11.0": "11",
                    "19045": "10 - 22H2",
                    "19044": "10 - 21H2",
                    "19043": "10 - 21H1",
                    "19042": "10 - 20H2",
                    "19041": "10 - 2004",
                    "18363": "10 - 1909",
                    "18362": "10 - 1903",
                    "17763": "10 - 1809",
                    "17134": "10 - 1803",
                    "16299": "10 - 1709",
                    "15063": "10 - 1703",
                    "14393": "10 - 1607",
                    "10586": "10 - 1511",
                    "10240": "10 - 1507",
                    "6.3.9600" : "8.1 / Server 2012 R2",
                    "6.2.9200" : "8 / Server 2012",
                    "6.1.7601" : "7 SP1",
                    "NT 10.0": "10",
                    "NT 6.3": "8.1 / Server 2012 R2",
                    "NT 6.2": "8 / Server 2012",
                    "NT 6.1": "7 / Server 2008 R2",
                    "NT 6.0": "Vista / Server 2008",
                    "NT 5.2": "XP x64 / Server 2003",
                    "NT 5.1": "XP",
                    "Windows XP": "XP",
                    "NT 5.01": "2000 SP1",
                    "NT 5.0": "2000",
                    "NT 4.0": "NT",
                    "98; Win 9x 4.90": "Me"
    }

    def getVersion(self, agent, word):
      if 'OS: ' in agent:
        v = agent.split('OS: ')[-1].split(' ')[0].strip()
        for key in self.win_versions.keys():
          if v in key:
            return self.win_versions.get(key)
        values = {key: value for key, value in self.win_versions.items() if key in v}
        #grab just the first value in case it is an empty dictionary and if so set to 'unknown'
        ver = next(iter(values.values()), None)
        if ver == None:
          ver = v
        return ver
      elif 'Windows-Update-Agent' in agent:
        #may be able to breakdown version to OS build at later date
        return 'Unknown'
      elif '.Win ' in agent:
        v = agent.split('.Win ')[-1].split(' ')[0].strip()
        return self.win_versions.get(v, v)
      elif 'Win32_' in agent:
        v = agent.split('Win32_')[-1].split('/')[0].strip()
        return self.win_versions.get(v, v)
      elif 'Win ' in agent:
        v = agent.split('Win ')[-1].split(';')[0].strip()
        return self.win_versions.get(v, v)
      elif 'Windows/' in agent:
        v = agent.split('Windows/')[-1].split(' ')[0].strip()
        for key in self.win_versions.keys():
          if v in key:
            return self.win_versions.get(key)
        values = {key: value for key, value in self.win_versions.items() if key in v}
        #grab just the first value in case it is an empty dictionary and if so set to 'unknown'
        ver = next(iter(values.values()), None)
        if ver == None:
          ver = v
        return ver
      elif 'PC-Windows;' in agent:
        v = agent.split('PC-Windows;')[-1].split(';')[0].strip()
        for key in self.win_versions.keys():
          if v in key:
            return self.win_versions.get(key)
        values = {key: value for key, value in self.win_versions.items() if key in v}
        #grab just the first value in case it is an empty dictionary and if so set to 'unknown'
        ver = next(iter(values.values()), None)
        if ver == None:
          ver = v
        return ver
      else:
        v = agent.split('Windows')[-1].replace(',', ';').split(';')[0].replace('/', '').strip()
        if ')' in v:
            v = v.split(')')[0]
        elif v == '':
          return 'Unknown'

        for key in self.win_versions.keys():
          if v in key:
            return self.win_versions.get(key)

        values = {key: value for key, value in self.win_versions.items() if key in v}
        #grab just the first value in case it is an empty dictionary and if so set to 'unknown'
        ver = next(iter(values.values()), None)
        if ver == None:
          ver = v
        return ver


class Ubuntu(Dist):
    look_for = ['Ubuntu', 'ubuntu']
    version_markers = ["/", " "]
    platform = 'Linux'


class Debian(Dist):
    look_for = 'Debian'
    skip_if_found = ["ubuntu"]
    version_markers = ["/", " "]
    platform = 'Linux'


class Fedora(Dist):
    look_for = 'Fedora'
    version_markers = ["/", " "]
    platform = 'Linux'


class RedHat(Dist):
    look_for = 'Red Hat'
    version_markers = ["/", " "]
    platform = 'Linux'


class Rocky(Dist):
    look_for = 'Rocky'
    version_markers = ["/", " "]
    platform = 'Linux'


class Gentoo(Dist):
    look_for = 'gentoo'
    version_markers = ["/", " "]
    platform = 'Linux'


class Mint(Dist):
    look_for = 'Mint'
    version_markers = ["/", " "]
    platform = 'Linux'

    def getVersion(self, agent, word):
        if 'Mint' in agent:
          return agent.split('Mint ')[-1].split(' ')[0]

class Tizen(Dist):
    look_for = 'Tizen'
    platform = 'Linux'
    version_markers = [("/", " "), (" ", ")")]

    def getModel(self, agent, word):
        if 'Samsung;' in agent:
          return 'Samsung: ' + agent.split('Samsung;')[-1].split(';')[0].strip()
        elif 'SMART-TV' in agent:
          return 'Smart TV'
        else:
          return 'Unknown'


class Chrome(Browser):
    look_for = ["Chrome", "CriOS"]
    version_markers = ["/", " "]
    skip_if_found = [" OPR", "Edge", "YaBrowser", "Edg/", "YandexBot", "bingbot", "amazonbot", "OPX", "GuardianBrowser"]

    def getVersion(self, agent, word):
        part = agent.split(word + self.version_markers[0])[-1]
        version = part.split(self.version_markers[1])[0]
        if '+' in version:
            version = version.split('+')[0]
        return version.strip()


class YaBrowser(Browser):
    look_for = "YaBrowser"
    name = "Yandex.Browser"
    version_markers = ["/", " "]

    def getVersion(self, agent, word):
        part = agent.split(word + self.version_markers[0])[-1]
        version = part.split(self.version_markers[1])[0]
        if '+' in version:
            version = version.split('+')[0]
        return version.strip()


#class ChromeiOS(Browser):
# this is just chrome browser on IOS, moving it to Chrome
#    look_for = "CriOS"
#    version_markers = ["/", " "]


class Chromecast(OS):
    look_for = ["CrKey"]
    platform = ' Chromecast'

    def getVersion(self, agent, word):
      if ('CrKey/' in agent):
        return agent.split('CrKey/')[-1].split(' ')[0]


class ChromeOS(OS):
    look_for = ["CrOS"]
    platform = ' ChromeOS'
    version_markers = [" ", " "]

    def getVersion(self, agent, word):
        version_markers = self.version_markers
        if word + '+' in agent:
            version_markers = ['+', '+']
        return agent.split(word + version_markers[0])[-1].split(version_markers[1])[1].strip()[:-1]


class Android(Dist):
    look_for = 'Android'
    platform = 'Android'
    skip_if_found = ['Windows Phone', 'Mac OS']

    android_versions = {
        #android SDK to OS Version
        #https://apilevels.com/
        #"adk version" : "android version"
        "20" : "4",
        "21" : "5.1",
        "22" : "5",
        "23" : "6",
        "24" : "7",
        "25" : "7.1",
        "26" : "8",
        "27" : "8.1",
        "28" : "8",
        "29" : "10",
        "30" : "11",
        "31" : "12",
        "32" : "12L",
        "33" : "13",
        "34" : "14",
        "35" : "15",
        "36" : "16",
        }

    def getVersion(self, agent, word):
      if ('Android/2' in agent) or ('Android/3' in agent):
        #convert if SDK 2x or 3x
        v = agent.split('Android/')[-1].split(' ')[0]
        v = self.android_versions.get(v, 'Unknown: Android/' + v)
        return v
      if 'Android ' in agent:
        return agent.split('Android ')[1].replace(')', ';').split(';')[0].strip()
      elif 'Android/' in agent:
        return agent.split('Android/')[1].replace(')', ';').split(' ')[0].split(';')[0].strip()
      else:
        return agent.split('Android')[-1].replace(')', ';').split(';')[0].strip()

    def getModel(self, agent, word):
        if ') Apple' in agent:
          i = agent.find(word) + len(word)
          m = agent[i:].replace(') Apple', ';').split(';')[1]
          #ugly fix for those without a model
          if m[0] == ' ':
            return m.strip()
          else:
            return 'Unknown'
        elif 'en_' in agent:
          #need to address other languages not just english versions, but works for my use case, but has another value in there sometime too, so more digging needed.
          return agent.split('en_')[-1].split(';')[1].strip()
        elif ('Android/2' in agent) or ('Android/3' in agent):
          return agent.split('(')[-1].split(')')[0].strip()
        elif ')' in agent:
          return agent.split(word)[-1].replace(')', ';').split(';')[1].strip()
        else:
          return 'Unknown'


class WebOS(Dist):
    look_for = 'hpwOS'

    def getVersion(self, agent, word):
        return agent.split('hpwOS/')[-1].split(';')[0].strip()


class NokiaS40(OS):
    look_for = 'Series40'
    platform = 'Nokia S40'

    def getVersion(self, agent, word):
        pass


class Symbian(OS):
    look_for = ['Symbian', 'SymbianOS']
    platform = 'Symbian'


class PlayStation(OS):
    look_for = ['PlayStation', 'PLAYSTATION']
    platform = 'PlayStation'
    version_markers = [" ", ")"]


class Xbox(OS):
    look_for = ['XBox', 'XboxOne']
    platform = 'XBox'
    version_markers = [" ", ")"]


class Axios(OS):
    look_for = 'axios'
    platform = 'axios'

    def getVersion(self, agent, word):
        return agent.split('/')[-1].strip()


class prefs:  # experimental
    os = dict(
        Linux=dict(dict(browser=[Firefox, Chrome], dist=[Ubuntu, Android])),
        BlackBerry=dict(dist=[BlackberryPlaybook]),
        Macintosh=dict(flavor=[MacOS]),
        Windows=dict(browser=[MSIE, Firefox]),
        ChromeOS=dict(browser=[Chrome]),
        Debian=dict(browser=[Firefox])
    )
    dist = dict(
        Ubuntu=dict(browser=[Firefox]),
        Android=dict(browser=[Safari]),
        IPhone=dict(browser=[Safari]),
        IPad=dict(browser=[Safari]),
    )
    flavor = dict(
        MacOS=dict(browser=[Opera, Chrome, Firefox, MSIE])
    )


detectorshub = DetectorsHub()


def detect(agent, fill_none=False):
    """
    fill_none: if name/version is not detected respective key is still added to the result with value None
    """
    result = dict(platform=dict(name=None, version=None))
    _suggested_detectors = []

    for info_type in detectorshub:
        detectors = _suggested_detectors or detectorshub[info_type]
        for detector in detectors:
            try:
                detector.detect(agent, result)
            except Exception as _err:
                pass

    if fill_none:
        for outer_key in ('os', 'browser'):
            outer_value = result.setdefault(outer_key, dict())
            for inner_key in ('name', 'version'):
                outer_value.setdefault(inner_key, None)

    return result


UNKNOWN_OS_NAME = 'Unknown OS'
UNKNOWN_BROWSER_NAME = 'Unknown Browser'


def simple_detect_tuple(agent, parsed_agent=None):
    """
    @params:
        agent::str
        parsed_agent::dict
            The result of detect, used to save calculations

    @return:
        (os_name, os_version, browser_name, browser_version)::Tuple(str)
    """
    result = parsed_agent or detect(agent)
    os_list = []
    if 'flavor' in result:
        os_list.append(result['flavor']['name'])
    if 'dist' in result:
        os_list.append(result['dist']['name'])
    if 'os' in result:
        os_list.append(result['os']['name'])

    os = os_list and " ".join(os_list) or UNKNOWN_OS_NAME
    os_version = os_list and (result.get('flavor') and result['flavor'].get('version')) or \
        (result.get('dist') and result['dist'].get('version')) or (result.get('os') and result['os'].get('version')) or ""
    browser = 'browser' in result and result['browser'].get('name') or UNKNOWN_BROWSER_NAME
    browser_version = 'browser' in result and result['browser'].get('version') or ""
    model = 'model' in result and result['model'] or ""

    return os, os_version, browser, browser_version, model


def simple_detect(agent, parsed_agent=None):
    """
    @params:
        agent::str
        parsed_agent::dict
            The result of detect, used to save calculations

    @return:
        (os_name_version, browser_name_version)::Tuple(str)
    """
    os, os_version, browser, browser_version, model = simple_detect_tuple(agent, parsed_agent=parsed_agent)
    if browser_version:
        browser = " ".join((browser, browser_version))
    if os_version:
        os = " ".join((os, os_version))
    return os, browser, model
