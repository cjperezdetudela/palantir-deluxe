import os
import sys
import time
import json
import urllib.parse

directory_items = []
resolved_url = None

def reset_shim_state():
    global directory_items, resolved_url
    directory_items = []
    resolved_url = None

class Monitor:
    def __init__(self):
        pass
    def waitForAbort(self, timeout=0):
        return False
    def abortRequested(self):
        return False

class Player:
    def __init__(self):
        pass
    def play(self, item="", listitem=None):
        global resolved_url
        print(f"[KODI PLAYER PLAY] item={item}")
        if item:
            resolved_url = item
        elif listitem and hasattr(listitem, "path"):
            resolved_url = listitem.path

    def isPlaying(self):
        return False

    def stop(self):
        pass

# --- XBMC ---
class XBMC:
    LOGINFO = 0
    LOGERROR = 1
    LOGWARNING = 2
    LOGDEBUG = 3
    Monitor = Monitor
    Player = Player

    @staticmethod
    def log(msg, level=0):
        print(f"[KODI LOG {level}] {msg}")

    @staticmethod
    def getCondVisibility(cond):
        return False

    @staticmethod
    def getInfoLabel(label):
        if 'System.BuildVersion' in label or 'System.Version' in label:
            return '20.0.0'
        if 'System.Language' in label:
            return 'Spanish'
        return ''

    @staticmethod
    def getRegion(id):
        return 'es'

    @staticmethod
    def getLanguage(format=0, region=False):
        return 'Spanish'

    @staticmethod
    def getSkinDir():
        return 'skin.estuary.palantir'

    @staticmethod
    def sleep(time_ms):
        time.sleep(time_ms / 1000.0)

    @staticmethod
    def executebuiltin(cmd):
        print(f"[KODI EXECUTEBUILTIN] {cmd}")

    @staticmethod
    def translatePath(path):
        base_dir = os.path.abspath(".")
        if path.startswith("special://database/"):
            db_dir = os.path.join(base_dir, "kodi_data", "database")
            os.makedirs(db_dir, exist_ok=True)
            return os.path.join(db_dir, path.replace("special://database/", ""))
        if path.startswith("special://home/"):
            home_dir = os.path.join(base_dir, "kodi_data", "home")
            os.makedirs(home_dir, exist_ok=True)
            return os.path.join(home_dir, path.replace("special://home/", ""))
        if path.startswith("special://profile/"):
            prof_dir = os.path.join(base_dir, "kodi_data", "profile")
            os.makedirs(prof_dir, exist_ok=True)
            return os.path.join(prof_dir, path.replace("special://profile/", ""))
        return os.path.join(base_dir, path)

# --- XBMCGUI ---
class ListItem:
    def __init__(self, label="", label2="", iconImage="", thumbnailImage="", path=""):
        self.label = label
        self.label2 = label2
        self.icon = iconImage or thumbnailImage
        self.thumbnail = thumbnailImage or iconImage
        self.path = path
        self.info = {}
        self.art = {}
        self.properties = {}

    def setInfo(self, type_str, infoLabels):
        if isinstance(infoLabels, dict):
            self.info.update(infoLabels)

    def setArt(self, artDict):
        if isinstance(artDict, dict):
            self.art.update(artDict)
            if 'thumb' in artDict and not self.thumbnail:
                self.thumbnail = artDict['thumb']
            if 'icon' in artDict and not self.icon:
                self.icon = artDict['icon']
            if 'poster' in artDict and not self.thumbnail:
                self.thumbnail = artDict['poster']
            if 'fanart' in artDict and not getattr(self, 'fanart', None):
                self.fanart = artDict['fanart']

    def setProperty(self, key, value):
        self.properties[key] = str(value)

    def getLabel(self):
        return self.label

    def setPath(self, path):
        self.path = path

class Dialog:
    def ok(self, heading, message):
        print(f"[KODI DIALOG OK] {heading}: {message}")
        return True

    def notification(self, heading, message, icon="", time=3000):
        print(f"[KODI DIALOG NOTIFY] {heading}: {message}")

    def select(self, heading, list_items):
        print(f"[KODI DIALOG SELECT] {heading}: {list_items}")
        return 0

class DialogProgress:
    def create(self, heading, message=""):
        pass

    def update(self, percent, message=""):
        pass

    def iscanceled(self):
        return False

    def close(self):
        pass

_window_properties = {}

class Window:
    def __init__(self, window_id=0):
        self.id = window_id

    def getProperty(self, key):
        return _window_properties.get(key, "")

    def setProperty(self, key, val):
        _window_properties[key] = str(val)

    def clearProperty(self, key):
        _window_properties.pop(key, None)

class WindowXMLDialog:
    def __init__(self, xml_file, script_path, default_skin="Default", default_res="720p"):
        pass
    def doModal(self):
        pass
    def close(self):
        pass
    def getControl(self, control_id):
        return None

class XBMCGUI:
    ListItem = ListItem
    Dialog = Dialog
    DialogProgress = DialogProgress
    Window = Window
    WindowXMLDialog = WindowXMLDialog
    NOTIFICATION_INFO = 'info'
    NOTIFICATION_WARNING = 'warning'
    NOTIFICATION_ERROR = 'error'

DB_DIR = os.path.abspath(os.path.join("kodi_data", "profile", "addon_data", "script.module"))
SETTINGS_FILE = os.path.abspath(os.path.join("kodi_data", "profile", "addon_data", "plugin.video.palantir3", "settings.json"))

def load_addon_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_addon_settings(settings_dict):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings_dict, f, indent=2)

class Addon:
    def __init__(self, addon_id="plugin.video.palantir3"):
        self.id = addon_id

    def getAddonInfo(self, info):
        info_lower = info.lower()
        if info_lower in ['path', 'profile']:
            return os.path.abspath(os.path.join("extracted_plugin.video.palantir3", "plugin.video.palantir3"))
        if info_lower == 'name':
            return "Palantir 3"
        if info_lower == 'version':
            return "3.3.11"
        return ""

    def getLocalizedString(self, id):
        return f"Text_{id}"

    def getSetting(self, id):
        st = load_addon_settings()
        val = st.get(id, "")
        if isinstance(val, bool):
            return "true" if val else "false"
        return str(val)

    def setSetting(self, id, val):
        st = load_addon_settings()
        st[id] = val
        save_addon_settings(st)

class XBMCADDON:
    Addon = Addon

# --- XBMCVFS ---
class XBMCVFS:
    @staticmethod
    def translatePath(path):
        return XBMC.translatePath(path)

    @staticmethod
    def exists(path):
        real_path = XBMC.translatePath(path)
        return os.path.exists(real_path)

    @staticmethod
    def mkdir(path):
        real_path = XBMC.translatePath(path)
        os.makedirs(real_path, exist_ok=True)

    @staticmethod
    def delete(path):
        real_path = XBMC.translatePath(path)
        if os.path.exists(real_path):
            try:
                os.remove(real_path)
            except:
                pass

class XBMCPLUGIN:
    @staticmethod
    def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=0):
        global directory_items
        item = {
            "url": url,
            "label": getattr(listitem, "label", ""),
            "icon": getattr(listitem, "icon", ""),
            "thumbnail": getattr(listitem, "thumbnail", ""),
            "fanart": getattr(listitem, "fanart", ""),
            "path": getattr(listitem, "path", ""),
            "info": getattr(listitem, "info", {}),
            "art": getattr(listitem, "art", {}),
            "properties": getattr(listitem, "properties", {}),
            "isFolder": isFolder
        }
        directory_items.append(item)
        return True

    @staticmethod
    def addDirectoryItems(handle, items, totalItems=0):
        for url, listitem, isFolder in items:
            XBMCPLUGIN.addDirectoryItem(handle, url, listitem, isFolder)
        return True

    @staticmethod
    def endOfDirectory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
        global directory_items
        return directory_items

    @staticmethod
    def setResolvedUrl(handle, succeeded, listitem):
        global resolved_url
        if succeeded and hasattr(listitem, "path"):
            resolved_url = listitem.path

# Install Shims into sys.modules
def install_kodi_shims():
    sys.modules['xbmc'] = XBMC
    sys.modules['xbmcgui'] = XBMCGUI
    sys.modules['xbmcaddon'] = XBMCADDON
    sys.modules['xbmcvfs'] = XBMCVFS
    sys.modules['xbmcplugin'] = XBMCPLUGIN
