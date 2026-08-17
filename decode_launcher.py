import base64
import codecs
import re

with open(r"extracted_plugin.video.palantir3\plugin.video.palantir3\default.py", "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

def get_var(name, text):
    m = re.search(r"^" + name + r"\s*=\s*'([^']+)'", text, re.MULTILINE)
    return m.group(1) if m else ""

def decode_b64(s):
    if not s: return ""
    rem = len(s) % 4
    if rem > 0: s += '=' * (4 - rem)
    return base64.b64decode(s).decode('utf-8', errors='ignore')

def decode_rot13(s):
    if not s: return ""
    return codecs.decode(s, 'rot13')

montolla = get_var("montolla", code)
farina = get_var("farina", code)
valderrama = get_var("valderrama", code)
elfary = get_var("elfary", code)

# Let's check how line 10 in default.py put them together:
# eval('montolla')+eval('codecs.decode(farina, "")')+eval('valderrama')+eval('codecs.decode(elfary, "rot13")')
# Notice: montolla is raw string, farina is string, valderrama is raw string, elfary is string rot13.
# The concatenated string is then b64decoded!

raw_concat = montolla + decode_rot13(farina) + valderrama + decode_rot13(elfary)
print(f"Raw concatenated base64 length: {len(raw_concat)}")

# Now base64 decode raw_concat!
rem = len(raw_concat) % 4
if rem > 0:
    raw_concat += '=' * (4 - rem)

try:
    final_python_code = base64.b64decode(raw_concat).decode('utf-8', errors='ignore')
    print("SUCCESSFULLY DECODED LAUNCHER!")
    with open("launcher_decoded.py", "w", encoding="utf-8") as f:
        f.write(final_python_code)
    print(f"Saved launcher_decoded.py (size: {len(final_python_code)} chars)")
except Exception as e:
    print(f"Base64 decode failed: {e}")
