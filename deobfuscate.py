import base64
import codecs
import re
import os

addon_dir = r"extracted_plugin.video.palantir3\plugin.video.palantir3"
default_py_path = os.path.join(addon_dir, "default.py")

with open(default_py_path, "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

def get_var(name, text):
    m = re.search(r"^" + name + r"\s*=\s*'([^']+)'", text, re.MULTILINE)
    return m.group(1) if m else None

def b64_decode_safe(s):
    if not s: return ""
    s = s.strip()
    missing_padding = len(s) % 4
    if missing_padding:
        s += '=' * (4 - missing_padding)
    return base64.b64decode(s).decode('utf-8', errors='ignore')

def rot13_decode_safe(s):
    if not s: return ""
    return codecs.decode(s, 'rot13')

montolla = get_var("montolla", code)
valderrama = get_var("valderrama", code)
farina = get_var("farina", code)
elfary = get_var("elfary", code)

out_code = ""
if montolla:
    out_code += "# --- MONTOLLA ---\n" + b64_decode_safe(montolla) + "\n"
if farina:
    out_code += "# --- FARINA ---\n" + rot13_decode_safe(farina) + "\n"
if valderrama:
    out_code += "# --- VALDERRAMA ---\n" + b64_decode_safe(valderrama) + "\n"
if elfary:
    out_code += "# --- ELFARY ---\n" + rot13_decode_safe(elfary) + "\n"

with open("default_decoded.py", "w", encoding="utf-8") as f:
    f.write(out_code)

print(f"Decoded default.py! Total size: {len(out_code)} chars")
