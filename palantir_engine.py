import os
import sys
import urllib.parse
import importlib.util

# 1. Install Kodi Shims
import kodi_shim
kodi_shim.install_kodi_shims()

# 2. Palantir Addon path setup
addon_path = os.path.abspath(os.path.join("extracted_plugin.video.palantir3", "plugin.video.palantir3"))
if addon_path not in sys.path:
    sys.path.insert(0, addon_path)

# Import decrypted launcher/default logic
default_script_path = os.path.abspath("downloaded_default_3.12.py")

def execute_palantir(params_str=""):
    """
    Simulates Kodi running plugin.video.palantir3 with given query params string.
    e.g. params_str = "?action=main" or "?action=pelis"
    """
    kodi_shim.reset_shim_state()
    
    # Setup sys.argv like Kodi
    sys.argv = [
        "plugin://plugin.video.palantir3/",
        "1",
        params_str
    ]
    
    # Execute default script in controlled globals dict
    global_scope = {
        '__file__': default_script_path,
        '__name__': '__main__',
        'sys': sys,
        'os': os,
        'xbmc': kodi_shim.XBMC,
        'xbmcgui': kodi_shim.XBMCGUI,
        'xbmcaddon': kodi_shim.XBMCADDON,
        'xbmcvfs': kodi_shim.XBMCVFS,
        'xbmcplugin': kodi_shim.XBMCPLUGIN,
    }
    
    try:
        with open(default_script_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        exec(code, global_scope)
    except SystemExit:
        pass
    except Exception as e:
        print(f"[PALANTIR ENGINE ERROR] Executing with params '{params_str}': {e}")
        
    return {
        "items": kodi_shim.directory_items,
        "resolved_url": kodi_shim.resolved_url
    }

if __name__ == "__main__":
    print("Testing Palantir Engine root listing...")
    result = execute_palantir("")
    print(f"Total root items returned: {len(result['items'])}")
    for item in result['items'][:10]:
        print(f" - [{item.get('label')}] -> {item.get('url')}")
