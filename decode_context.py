import base64
import codecs
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"extracted_plugin.video.palantir3\plugin.video.palantir3\context.py", "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

def get_var(name, text):
    m = re.search(r"^" + name + r"\s*=\s*'([^']+)'", text, re.MULTILINE)
    return m.group(1) if m else None

def decode_b64_truncate(s):
    if not s: return ""
    rem = len(s) % 4
    if rem > 0:
        s = s[:-rem]
    return base64.b64decode(s).decode('utf-8', errors='ignore')

montolla = get_var("montolla", code)
valderrama = get_var("valderrama", code)
farina = get_var("farina", code)
elfary = get_var("elfary", code)

print("=== CONTEXT.PY MONTOLLA ===")
print(decode_b64_truncate(montolla))

print("\n=== CONTEXT.PY VALDERRAMA ===")
print(decode_b64_truncate(valderrama))
