import base64
import codecs
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("downloaded_default_3.12.py", "r", encoding="utf-8", errors="ignore") as f:
    code = f.read()

print("File size:", len(code))
print("First 20 lines:")
for l in code.splitlines()[:20]:
    print("  ", l)

# Check variable definitions like in previous files
montolla = re.search(r"montolla='([^']+)'", code)
farina = re.search(r"farina='([^']+)'", code)
valderrama = re.search(r"valderrama='([^']+)'", code)
elfary = re.search(r"elfary='([^']+)'", code)

if montolla and farina and valderrama and elfary:
    print("\nVariables found! Attempting full decode...")
    m_str = montolla.group(1)
    f_str = codecs.decode(farina.group(1), 'rot13')
    v_str = valderrama.group(1)
    e_str = codecs.decode(elfary.group(1), 'rot13')
    
    raw_concat = m_str + f_str + v_str + e_str
    rem = len(raw_concat) % 4
    if rem > 0: raw_concat += '=' * (4 - rem)
    
    decoded = base64.b64decode(raw_concat).decode('utf-8', errors='ignore')
    with open("palantir_core_3.12.py", "w", encoding="utf-8") as out:
        out.write(decoded)
    print(f"Decoded core script saved to palantir_core_3.12.py (size: {len(decoded)} chars)")
