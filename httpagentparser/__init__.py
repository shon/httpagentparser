"""
Extract client information from http user agent
The module does not try to detect all capabilities of browser in current form (it can easily be extended though).
Aim is
    * fast
    * very easy to extend
    * reliable enough for practical purposes
    * and assist python web apps to detect clients.
"""
import sys

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
    def reorderByPrefs(self, detectors, prefs):
        if prefs == None:
            return []
        elif prefs == []:
            return detectors
        else:
            prefs.insert(0, '')
            return sorted(detectors, key=lambda d: d.name in prefs and prefs.index(d.name) or sys.maxint)
    def __iter__(self):
        return iter(self._known_types)
    def registerDetectors(self):
        detectors = [v() for v in globals().values() if DetectorBase in getattr(v, '__mro__', [])]
        for d in detectors:
            if d.can_register:
                self.register(d)

class DetectorBase(object):
    name = "" # "to perform match in DetectorsHub object"
    info_type = "override me"
    result_key = "override me"
    order = 10 # 0 is highest
    look_for = "string to look for"
    can_register = False
    prefs = dict() # dict(info_type = [name1, name2], ..)
    version_splitters = ["/", " "]
    _suggested_detectors = None
    def __init__(self):
        if not self.name:
            self.name = self.__class__.__name__
        self.can_register = (self.__class__.__dict__.get('can_register', True))
    def detect(self, agent, result):
        # -> True/None
        if self.checkWords(agent):
            result[self.info_type] = dict(name = self.name)
            version = self.getVersion(agent)
            if version:
                result[self.info_type]['version'] = version
            return True
    def checkWords(self, agent):
        # -> True/None
        if self.look_for in agent:
            return True
    def getVersion(self, agent):
        # -> version string /None
        return agent.split(self.look_for + self.version_splitters[0])[-1].split(self.version_splitters[1])[0].strip()

class OS(DetectorBase):
    info_type = "os"
    can_register = False
    version_splitters = [";", " "]

class Dist(DetectorBase):
    info_type = "dist"
    can_register = False

class Flavor(DetectorBase):
    info_type = "flavor"
    can_register = False

class Browser(DetectorBase):
    info_type = "browser"
    can_register = False

class Macintosh(OS):
    look_for = 'Macintosh'
    prefs = dict(dist = None)
    def getVersion(self, agent): pass

class Firefox(Browser):
    look_for = "Firefox"

class Konqueror(Browser):
    look_for = "Konqueror"
    version_splitters = ["/", ";"]

class Opera(Browser):
    look_for = "Opera"

class MSIE(Browser):
    look_for = "MSIE"
    name = "Microsoft Internet Explorer"
    version_splitters = [" ", ";"]

class Galeon(Browser):
    look_for = "Galeon"

class Safari(Browser):
    look_for = "Safari"
    def checkWords(self, agent):
        unless_list = ["Chrome", "OmniWeb"]
        if self.look_for in agent:
            for word in unless_list:
                if word in agent:
                    return False
            return True
    def getVersion(self, agent):
        if "Version/" in agent:
            return agent.split('Version/')[-1].split(' ')[0].strip()
        else:
            return agent.split('Safari ')[-1].split(' ')[0].strip() # Mobile Safari

class Linux(OS):
    look_for = 'Linux'
    prefs = dict(browser = ["Firefox"], dist=["Ubuntu"], flavor=None)
    def getVersion(self, agent): pass

class Macintosh(OS):
    look_for = 'Macintosh'
    prefs = dict (dist = None, flavor = ['MacOS'])
    def getVersion(self, agent): pass

class MacOS(Flavor):
    look_for = 'Mac OS'
    prefs = dict (browser = ['Firefox', 'Opera', "Microsoft Internet Explorer"])
    def getVersion(self, agent):
        version_end_chars = [';', ')']
        part = agent.split('Mac OS')[-1].strip()
        version_list = []
        for c in part:
            if c in version_end_chars:
                break
            version_list.append(c)
        version = ''.join(version_list).replace('_', '.')
        return version

class Windows(OS):
    look_for = 'Windows'
    prefs = dict (browser = ["Microsoft Internet Explorer", 'Firefox'], dict = None, flavor = None)
    def getVersion(self, agent):
        return agent.split('Windows')[-1].split(';')[0].strip()

class Ubuntu(Dist):
    look_for = 'Ubuntu'
    version_splitters = ["/", " "]
    prefs = dict (browser = ['Firefox'])

class Debian(Dist):
    look_for = 'Debian'
    version_splitters = ["/", " "]
    prefs = dict (browser = ['Firefox'])

class Chrome(Browser):
    look_for = "Chrome"
    version_splitters = ["/", " "]

detectorshub = DetectorsHub()

def detect(agent):
    result = dict()
    prefs = dict ()
    _suggested_detectors = []
    for info_type in detectorshub:
        if not _suggested_detectors:
            detectors = detectorshub[info_type]
            _d_prefs = prefs.get(info_type, [])
            detectors = detectorshub.reorderByPrefs(detectors, _d_prefs)
            if "detector" in locals():
                detector._suggested_detectors = detectors
        else:
            detectors = _suggested_detectors
        for detector in detectors:
            #print "detector name: ", detector.name
            if detector.detect(agent, result):
                prefs = detector.prefs
                _suggested_detectors = detector._suggested_detectors
                break
    return result

class Result(dict):
    def __missing__(self, k):
        return ""

def detect(agent):
    result = Result()
    _suggested_detectors = []
    for info_type in detectorshub:
        detectors = _suggested_detectors or detectorshub[info_type]
        for detector in detectors:
            if detector.detect(agent, result):
                if detector.prefs and not detector._suggested_detectors:
                    _suggested_detectors = detectorshub.reorderByPrefs(detectors, detector.prefs.get(info_type))
                    detector._suggested_detectors = _suggested_detectors
                    break
    return result

def simple_detect(agent):
    """
    -> (os, browser) # tuple of strings
    """
    result = detect(agent)
    os_list = []
    if 'flavor' in result: os_list.append(result['flavor']['name'])
    if 'dist' in result: os_list.append(result['dist']['name'])
    if 'os' in result: os_list.append(result['os']['name'])

    os = os_list and " ".join(os_list) or "Unknown OS"
    os_version = os_list and (result['flavor'] and result['flavor'].get('version')) or (result['dist'] and result['dist'].get('version')) or (result['os'] and result['os'].get('version')) or ""
    browser = 'browser' in result and result['browser']['name'] or 'Unknown Browser'
    browser_version = 'browser' in result and result['browser'].get('version') or ""
    if browser_version:
        browser = " ".join((browser, browser_version))
    if os_version:
        os = " ".join((os, os_version))
    return os, browser

def test():
    import datetime
    #execfile("testdata", globals())
    agents = [
       "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10",
       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_6) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24,gzip(gfe)"
        ]
    then = datetime.datetime.now()
    for agent in agents * 10:
        print agent
        #print detect(agent)
        print "* ", simple_detect(agent)
    #s = "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-GB; rv:1.9.0.10) Gecko/2009042315 Firefox/3.0.10"
    #print s
    #print detect(s)
    now = datetime.datetime.now()
    print len(agents), "analysed in ", now - then

if __name__ == '__main__':
    test()
